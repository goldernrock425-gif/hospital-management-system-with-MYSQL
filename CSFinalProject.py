import os
import platform
import mysql.connector

# -------------------- DATABASE CONNECTION --------------------
# Connect to MySQL and create database if it does not exist
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2806"
)
mycursor = mydb.cursor()

# Create the 'school' database and use it
mycursor.execute("CREATE DATABASE IF NOT EXISTS Patient")
mycursor.execute("USE Patient")

mycursor.execute("DROP TABLE IF EXISTS Patient_details")


mycursor.execute("""
    CREATE TABLE Patient_details (
        idno INT PRIMARY KEY,
        name VARCHAR(20),
        age INT,
        contact VARCHAR(10)
    )
""")

# -------------------- MAIN PROGRAM LOOP --------------------
exit_program = 'n'

while exit_program == 'n':
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print('*' * 200)
    print('|' + ' ' * 32 + '\t\tHOSPITAL MANAGEMENT SYSTEM' + ' ' * 32 + '|')
    print('*' * 200)
    print('[ 1 ] Insert Patient Record |', end='')
    print(' [ 2 ] View Patient Record |', end='')
    print(' [ 3 ] Update Patient Record |', end='')
    print(' [ 4 ] Delete Records |', end='')
    print(' [ 5 ] EXIT |')
    print('\n' + '*' * 200)

    ch = input('YOUR Choice (1/2/3/4/5): ')


    if ch == '1':
        choice = 'y'
        while choice == 'y':
            try:
                sidno = int(input('Enter the ID number of Patient: '))
                sname = input('Enter the name of Patient: ')
                sage = int(input('Enter the age of Patient: '))
                scontact = input('Enter the contact number of Patient: ')
                qry = "INSERT INTO Patient_details (idno, name, age, contact) VALUES (%s, %s, %s, %s)"
                data = (sidno, sname, sage, scontact)
                mycursor.execute(qry, data)
                mydb.commit()
                print('RECORD INSERTED SUCCESSFULLY')
            except mysql.connector.IntegrityError:
                print("Error: A Patient with this ID already exists.")
            except ValueError:
                print("Invalid input. Please enter valid data types.")
            choice = input('Do you wish to insert more records (y/n)? ').lower()

    elif ch == '2':
        choice = 'y'
        while choice == 'y':
            try:
                idno = int(input('Enter the ID number of Patient to search: '))
                qry = "SELECT * FROM Patient_details WHERE idno = %s"
                mycursor.execute(qry, (idno,))
                result = mycursor.fetchall()
                if result:
                    for (idno, name, age, contact) in result:
                        print('-----------------------------------')
                        print('Patient ID No   :', idno)
                        print('Patient Name    :', name)
                        print('Patient Age     :', age)
                        print('Patient Contact :', contact)
                        print('-----------------------------------')
                else:
                    print("No record found with this ID.")
            except ValueError:
                print("Invalid input. ID must be a number.")
            choice = input('Do you wish to search more records (y/n)? ').lower()

    elif ch == '3':
        choice = 'y'
        while choice == 'y':
            try:
                idno = int(input('Enter the ID number of Patient to update: '))
                new_name = input('Enter new name: ')
                new_age = int(input('Enter new age: '))
                new_contact = input('Enter new contact number: ')
                qry = "UPDATE Patient_details SET name = %s, age = %s, contact = %s WHERE idno = %s"
                mycursor.execute(qry, (new_name, new_age, new_contact, idno))
                if mycursor.rowcount == 0:
                    print("No record found to update.")
                else:
                    mydb.commit()
                    print('RECORD UPDATED SUCCESSFULLY')
            except ValueError:
                print("Invalid input. Please enter correct data types.")
            choice = input('Do you wish to update more records (y/n)? ').lower()

    elif ch == '4':
        choice = 'y'
        while choice == 'y':
            try:
                idno = int(input('Enter the ID number of Patient to delete: '))
                qry = "DELETE FROM Patient_details WHERE idno = %s"
                mycursor.execute(qry, (idno,))
                if mycursor.rowcount == 0:
                    print("No record found to delete.")
                else:
                    mydb.commit()
                    print('RECORD DELETED SUCCESSFULLY')
            except ValueError:
                print("Invalid input. ID must be a number.")
            choice = input('Do you wish to delete more records (y/n)? ').lower()

    elif ch == '5':
        print("\n\t\tThanks for using Hospital Management System...")
        print("\t\t----------------------------------------------")
        break


    else:
        print('\n\t\tError: Not a valid option.')
        print('\t\tValid options are: "i", "v", "u", "d", "e".')

    # Ask to exit after each operation
    if ch != '5':
        exit_program = input('\nDo you wish to exit the program (y/n)? ').lower()
