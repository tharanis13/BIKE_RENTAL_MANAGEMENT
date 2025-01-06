import time
from getpass import getpass
import mysql.connector 
from tabulate import tabulate

con = mysql.connector.connect( host="localhost", user="root", password="1234", database="bike_rental") 
cursor = con.cursor()

def adminrental():
    while 1:
        print("\n1.Add New Bike\n2.Update Availability\n3.Rental details\n4.Rental history\n\033[1mor 5.Logout\033[0m\n")
        user_choice1=int(input("Enter the option:"))
        if user_choice1 == 1:
            brand=input("\nEnter the brand name:")
            name=input("Enter name:")
            model=input("Enter model:")
            availability="A"
            query="INSERT INTO bike(brand, name, model, availability) VALUES (%s,%s,%s,%s)"
            cursor.execute(query,(brand,name,model,availability))
            con.commit()
            print("\n\033[1mAdded Successfully\033[0m")
        elif user_choice1 == 2:
            brand=input("Enter the brand name:")
            name=input("Enter name:")
            availability=input("Enter the Availability:")
            query="UPDATE bike SET availability=%s WHERE brand=%s and name=%s"
            cursor.execute(query,(availability,brand,name))
            con.commit()
            print("\n\033[1mUpdated Successfully\033[0m\n")
        elif user_choice1 == 3:
            query="SELECT billnumber,customer,phonenumber,brand,name FROM rental WHERE process='On_rental'"
            cursor.execute(query)
            table = cursor.fetchall() 
            print('\nRental data:') 
            headers = ["Billno.","Customer","Phone","Brand","Name"]
            print(tabulate(table, headers=headers, tablefmt="psql"))    
            time.sleep(0.8)
        elif user_choice1 == 4:
            query="SELECT * FROM rental"
            cursor.execute(query)
            table1 = cursor.fetchall() 
            print('\nRental history:') 
            headers =["Billno.","Customer","Phone","Brand","Name","Process","Revenue"]
            print(tabulate(table1, headers=headers, tablefmt="psql"))
            time.sleep(0.8)
        elif user_choice1 == 5:
            break
        else:
            print("Invalid option!!\n")

def existing_user():
    print("\n\033[1mCREDENTIALS:\033[0m")
    user_name = input("User name: ")
    password = getpass()
    query = "SELECT * FROM user_detail WHERE name = %s AND password = %s"
    cursor.execute(query, (user_name, password))
    result = cursor.fetchone()
    if result:
        print("\n\033[1mWelcome back, {}!\033[0m\n".format(user_name))
        time.sleep(0.8)
        adminrental()
    else:
        print("Invalid username or password.")
        time.sleep(0.8)
        admin()
    time.sleep(0.8)

def new_user():
    database_password=getpass(prompt="\nEnter the database password to get access:")
    if database_password.lower() == "root":
        print("\n\033[1mAccess Granted!!\033[0m\n")
        user_name = input("User name:")
        phonenumber = int(input("Phonenumber:"))
        password = getpass()
        query="INSERT INTO user_detail(name, phonenumber, password) VALUES (%s,%s,%s)"
        cursor.execute(query,(user_name,phonenumber,password))
        con.commit()
        print("\n\033[1mUser created successfully\033[0m\n")
        adminrental()
    time.sleep(0.8)

def booking():
    print("\n\033[1mWelcome!!\033[0m")
    print("\n\033[1mATTENTION TO THE CUSTOMERS!!!\033[0m")
    print("1.Please enter valid details.\n2.Provide photocopy of Aadhar card and Driving License.\n3.In case of any damage service charge will be issued from the customer.\n\033[1mCharge : Rs.7/h\033[0m\n")
    print("\n\033[1mEnter Your details\033[0m")
    customer=input("Name:")
    phonenumber = int(input("Phonenumber:"))
    brand=input("Brand:")
    name=input("Model Name:")
    availability="A"
    process="On_rental"
    query="SELECT brand,name,availability FROM bike WHERE brand=%s and name=%s and availability=%s"
    cursor.execute(query,(brand,name,availability))
    found=cursor.fetchall()
    if found:
        query1="INSERT INTO rental(billnumber, customer, phonenumber, brand, name, process) VALUES (%s,%s,%s,%s,%s,%s)"
        availability="N/A"
        query2="UPDATE bike SET availability=%s WHERE brand=%s and name=%s"
        cursor.execute(query2,(availability,brand,name))
        query3="SELECT MAX(billnumber) FROM rental"
        cursor.execute(query3)
        billnumber=cursor.fetchone()
        if billnumber[0] is None:
            billnumber = 1 
        else:
            billnumber = billnumber[0] + 1
        cursor.execute(query1,(billnumber,customer,phonenumber,brand,name,process))
        con.commit()
        print("\nThank you for rental")
        print("Your bill number is {}".format(billnumber))

    else:
        print("\nBike Not Available!!")

def billing():
    bill=int(input("Enter your Bill number:"))
    phonenumber=int(input("Enter your phone number:"))
    process_old="On_rental"
    process_new="Completed"
    availability="A"
    query="SELECT * FROM rental WHERE billnumber=%s and phonenumber=%s and process=%s"
    cursor.execute(query,(bill,phonenumber,process_old))
    result=cursor.fetchall()
    if result:
        brand=result[0][3]
        name=result[0][4]
        days=float(input("Enter the number of days rented:"))
        query1="UPDATE bike SET availability=%s WHERE brand=%s and name=%s"
        cursor.execute(query1,(availability,brand,name))
        amount=days*7*24
        query2="UPDATE rental SET process=%s,revenue=%s WHERE billnumber=%s and phonenumber=%s"
        cursor.execute(query2,(process_new,amount,bill,phonenumber))
        con.commit()
        time.sleep(0.8)
        print("\nYour rental details:")
        for row in result: 
            print("Bill number: {}".format(row[0]))
            print("Customer Name: {}".format(row[1]))
            print("Phonenumber: {}".format(row[2])) 
            print("Brand: {}".format(row[3]))
            print("Name: {}".format(row[4]))
            print("\n\033[1mTotal bill: {}\033[0m".format(amount))
            print("\nThank you for using our service.")
    else:
        print("Invalid Details!!")

def check():
    availability="A"
    query="SELECT brand,name FROM bike WHERE availability=%s"
    cursor.execute(query,(availability,))
    table=cursor.fetchall()
    headers = ["Brand","Name"]
    print(tabulate(table, headers=headers, tablefmt="psql"))
    customer()

def admin():
    print("\n\033[1mADMIN\033[0m")
    print("1.Existing admin\n2.New admin\n\033[1mor 3.Exit admin\033[0m")
    user_choice1=int(input("\nSelect the admin/exit:"))
    time.sleep(0.8)
    while user_choice1 != 0:
        if user_choice1 == 1:
            existing_user()
            user_choice1 = 0
        elif user_choice1 == 2:
            new_user()
            user_choice1 = 0
        elif user_choice1 == 3:
            break
        else:
            print("Invalid choice!!")


def customer():
    print("\n1.New Booking\n2.Billing\n3.Check Availability\n\033[1mor 4.Exit customer\033[0m\n")
    user_choice1=int(input("Select the option/exit:"))
    time.sleep(0.8)
    while user_choice1 != 0:
        if user_choice1 == 1:
            booking()
            user_choice1 = 0
        elif user_choice1 == 2:
            billing()
            user_choice1 = 0
        elif user_choice1 == 3:
            check()
            user_choice1=0
        elif user_choice1 == 4:
            break
        else:
            print("Invalid choice!!")
            admin()

def main():
    print("-"*160)
    print("\033[1mEZ Bike Rentals\033[0m".center(165))
    print("-"*160)
    while 1:
        print("\n\033[1mLOGIN AS\033[0m")
        print("1.Admin\n2.Customer\n\033[1mor 3.Exit App\033[0m")
        user_choice1=int(input("\nSelect the user/exit:"))
        time.sleep(0.8)
        if user_choice1 == 1:
            admin()
            break
        elif user_choice1 == 2:
            customer()
            break
        elif user_choice1 == 3:
            break
        else:
            print("Invalid choice!!")

main()
cursor.close() 
con.close()
