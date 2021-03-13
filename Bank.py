from mysql import connector
from mysql.connector import Error as e
def ConnectDB():
    try:
        conn = connector.connect(host="localhost",
                                 db='bank_application',
                                 user='root',
                                 password='root')
        if conn.is_connected():
            db_info = conn.get_server_info()
            print("Connected to mysql server version is", db_info)
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to databse", record)
    except e:
        print("Error while connecting to Mysql", e)
    return conn
conn = ConnectDB()
def Create_Table(conn):
    try:
        Query = '''CREATE TABLE IF NOT EXISTS New_bank_Account(
        ID int not null auto_increment,
        FirstName varchar(20) not null,
        LastName varchar(20) not null,
        Email varchar(25) not null,
        Mobile_Number varchar(10) not null,
        Gender varchar(1) not null,
        Date_Of_Birth Date not null,
        Aadhar_Number varchar(12) not null,
        Address varchar(100) not null,
        City varchar(50) not null,
        State varchar(50) not null,
        Country varchar(50) not null,
        Balance double not null,
        Password varchar(12) not null,
        primary key(id)
        )'''
        cursor = conn.cursor()
        cursor.execute(Query)
        print("Database connected Successfully...!!")
    except e:
        print(f"Database already Connected...!!: {e}")

def Create_Account(conn,FirstName, LastName, Email, Mobile_Number, Gender, Date_Of_Birth,
                   Aadhar_Number, Address, City, State, Country, Balance, Password):
    try:
        Query = """INSERT INTO New_bank_Account(FirstName, LastName, Email,
        Mobile_Number, Gender, Date_Of_Birth, Aadhar_Number, Address,
        City, State, Country, Balance, Password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor = conn.cursor()
        cursor.execute(Query,(FirstName, LastName, Email, Mobile_Number, Gender,
                               Date_Of_Birth, Aadhar_Number, Address, City, State, Country, Balance, Password))
        conn.commit()
        print("Your Details Has Been Stored")
    except e:
        print(f"Failed to stored account details {e}")

def FetchBalance(conn, id):
    Query ='''SELECT Balance FROM New_bank_Account where ID = %s'''
    cursor = conn.cursor()
    cursor.execute(Query,(id,))
    record = cursor.fetchall()
    for val in record:
        bal = val[0]
    return bal

def FetchPassword(conn, id):
    Query = '''SELECT Password FROM New_bank_Account where ID = %s'''
    cursor = conn.cursor()
    cursor.execute(Query, (id,))
    record = cursor.fetchall()
    for val in record:
        passw = val[0]
    return passw

def FetchAccountID(conn, id):
    Query = '''SELECT ID FROM New_bank_Account where ID = %s'''
    cursor = conn.cursor()
    cursor.execute(Query, (id,))
    record = cursor.fetchall()
    for val in record:
        ID = val[0]
    return ID


def ViewAccount(conn,id):
    try:
        Query ='''SELECT * FROM New_bank_Account where ID = %s'''
        cursor = conn.cursor()
        cursor.execute(Query, (id,))
        records = cursor.fetchall()
        for row in records:
            print("******************* ACCOUNT DETAILS **********************")
            print(f"Your ID = {row[0]}" )
            print(f"Your Name = {row[1]} {row[2]}")
            print(f"Email ID = {row[3]}")
            print(f"Mobile   = {row[4]}")
            print(f"Gender = {row[5]}")
            print(f"Date of Birth = {row[6]}")
            print(f"Aadhar Number = {row[7]}")
            print(f"Address= {row[8]}, {row[9]}, {row[10]}, {row[11]}")
            print(f"Balance = {row[11]}")
            print("**********************************************************")
    except e:
        print(f"Unable to view your account details...{e}")
def DepositAmt(conn, Deposit_amt, id):
    try:
        balAmt = FetchBalance(conn,id)
        Add_bal = balAmt + Deposit_amt
        Query ='''UPDATE New_bank_Account SET Balance = %s WHERE ID = %s'''
        cursor = conn.cursor()
        cursor.execute(Query,(Add_bal,id))
        conn.commit()
        print("Your Amount Has Been Deposited Successfully..!")
        print(f"Your Present Balance is: {FetchBalance(conn,id)}")
    except e:
        print(f"Unable to Deposit Amount in your Account: {e} ")

def WithdrawAmt(conn, withdraw_amt, id):
    try:
        balAmt = FetchBalance(conn,id)
        debit_bal = balAmt - withdraw_amt
        Query ='''UPDATE New_bank_Account SET Balance = %s WHERE ID = %s'''
        cursor = conn.cursor()
        cursor.execute(Query,(debit_bal,id))
        conn.commit()
        print(f"Your {withdraw_amt} Has Been Withdraw Successfully..!")
        print(f"Your Present Balance is: {FetchBalance(conn,id)}")
    except e:
        print(f"Unable to Deposit Amount in your Account: {e} ")

def UpdateAccount(conn, id, choice):
    if choice == '1':
        try:
            print("Updating the Email...")
            new_Email = input("Enter the New Email ID: ")
            Query = """Update New_bank_Account set Email = %s where ID = %s"""
            cursor = conn.cursor()
            cursor.execute(Query, (new_Email, id))
            conn.commit()
            print("Your Email Address is Updated Successfully...!")
        except e:
            print(f"Unable to update your email: {e}")
    elif choice == '2':
        try:
            print("Updating the Mobile Number...")
            mobile_Number = input("Enter the New Mobile Number: ")
            Query = """Update New_bank_Account set Mobile_Number = %s where ID = %s"""
            cursor = conn.cursor()
            cursor.execute(Query, (mobile_Number, id))
            conn.commit()
            print("Your Mobile Number is Updated Successfully...!")
        except e:
            print(f"Unable to update your Mobile Number: {e}")

    elif choice == '3':
        try:
            print("Updating the Password...")
            password = input("Enter the Password: ")
            Query = """Update New_bank_Account set Password = %s where ID = %s"""
            cursor = conn.cursor()
            cursor.execute(Query, (password, id))
            conn.commit()
            print("Your New Password is Updated Successfully, Login again to verify...!")
        except e:
            print(f"Unable to update your Password: {e}")


def Close_Account(conn, id):
    try:
        Query = """DELETE FROM New_bank_Account where ID = %s"""
        cursor = conn.cursor()
        cursor.execute(Query, (id,))
        conn.commit()
        print("Account Closed Successfully")
    except e:
        print(f"Failed to close your account")


Appclose = True
while Appclose:
    Create_Table(conn)
    print("Enter the following choice:")
    print("************************************************************")
    print("==========    WELCOME TO INDIAN BANKING SYSTEM    ==========")
    print("************************************************************")
    print("==========     (A). Login with Account          ============")
    print("==========     (B). Open New Client Account     ============")
    print("==========     (C). Exit                        ============")
    choice = input("Enter your Choice: ")

    if choice == 'A':
        print("************************************************************")
        print("==========   INDIAN BANKING SYSTEM LOGIN SYSTEM   ==========")
        print("************************************************************")
        ID = int(input("Enter your Account ID: "))
        if ID == FetchAccountID(conn,ID):
            print("Account ID is Valid")
        else:
            print("You have entered Invalid ID")
        password = input("Enter your Password: ")
        if password == FetchPassword(conn,ID):
            print("Account is Verified...")

            while userClose:
                print("************************************************************")
                print("==========    WELCOME TO INDIAN BANKING SYSTEM    ==========")
                print("************************************************************")
                print("Enter the following choice.....:")
                print("==========     (A). View Your Account Details   ============")
                print("==========     (B). The Client Withdraw a Money ============")
                print("==========     (C). The Client Deposit a Money  ============")
                print("==========     (D). Modify account details      ============")
                print("==========     (E). Close My Account            ============")
                print("==========     (F). Quit                        ============")
                print("************************************************************")
                Create_Table(conn)
                choice = input("Your choice is: ")

                if choice == 'A':
                    id = int(input("Enter your ID: "))
                    ViewAccount(conn, id)

                elif choice == 'B':
                    id = int(input("Enter your ID: "))
                    withdrawAmount = float(input("Enter the Amount to withdraw: "))
                    WithdrawAmt(conn, withdrawAmount, id)

                elif choice == 'C':
                    id = int(input("Enter your ID: "))
                    DepositAmount = float(input("Enter the Amount: "))
                    DepositAmt(conn,DepositAmount,id)

                elif choice == 'D':
                    back = True
                    while back:
                        print("To Update your Account, Enter the following choice:")
                        print("************************************************************")
                        print("================ WELCOME TO UPDATE CENTER ==================")
                        print("************************************************************")
                        print("===========     (1). To Update Email            ============")
                        print("===========     (2). To Update Mobile Number    ============")
                        print("===========     (3). To Update Password         ============")
                        print("===========     (4). Back To Main Menu          ============")
                        print("************************************************************")
                        option = input("Enter Choice to Update: ")
                        id = int(input("Enter Your Account ID: "))
                        UpdateAccount(conn,id,option)
                        if option == '4':
                            back = False
                elif choice == 'E':
                    id = int(input("Enter your Account ID: "))
                    print("===========  Are You Sure to Wanna Delete Your Account Permanently (Yes & No) ============")
                    yesNo = input("Please Enter Yes or No: ")
                    if yesNo == "Yes":
                        Close_Account(conn, id)
                    else:
                        print("Thanks to keep connecting with us...")

                elif choice == 'F':
                    print("Good Bye...! See you Again")
                    userClose = False
        else:
            print("Password is Wrong..Login Again..!")

    elif choice == 'B':
        print("*************************************************************")
        print("= WELCOME TO INDIAN BANKING SYSTEM NEW ACCOUNT REGISTRATION =")
        print("*************************************************************")
        First_Name = input("Your First Name: ")
        Last_Name = input("Your Last Name: ")
        Email = input("Your MailID: ")
        Password = input("Enter Any Password: ")
        Mobile_Number = input("Your Mobile number: ")
        Gender = input("Your Gender: ")
        Date_Of_Birth = input("Your DOB (yyyy-mm-dd): ")
        Aadhar_Number = input("Your Aadhar Number: ")
        Address = input("Your Address: ")
        City = input("Your City: ")
        State = input("Your State: ")
        Country = input("Your Country: ")
        Balance = input("How much money you want to deposit: ")
        Create_Account(conn, First_Name, Last_Name, Email, Mobile_Number, Gender, Date_Of_Birth,
                       Aadhar_Number, Address, City, State, Country, Balance, Password)

    elif choice == "C":
        print("Good Bye...! See you Again")
        Appclose = False