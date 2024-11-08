
import random
import mysql.connector as sql
import datetime as dt

mydb = sql.connect(host='localhost', user='root', passwd='12345')
c = mydb.cursor(buffered=True)
c.execute('use bank')


def tables():
    try:
        c.execute('create database if not exists bank')
        c.execute('use bank')
        c.execute('create table if not exists bank_customer(acno integer primary key, username varchar(20), password varchar(255), name varchar(20), mobile_no integer, city varchar(20), date date)')
        c.execute(
            'create table if not exists bank_transactions(acno integer primary key, balance decimal(20,4))')
        c.execute(
            'create table if not exists bank_report_deposit(acno integer, date date, time char(9), deposit decimal(20,4))')
        c.execute(
            'create table if not exists bank_report_withdraw(acno integer, date date, time char(9), withdraw decimal(20,4))')
        mydb.commit()
    except sql.Error as err:
        print(f"Database setup error: {err}")


def create_account():
    try:
        print('----------------------------------')
        u = input('Enter your username to be created: ')
        print('----------------------------------')
        p = input('Enter password: ')
        print('----------------------------------')
        a = input('Enter name: ')
        print('----------------------------------')
        b = int(input('Enter your mobile no.: '))
        print('----------------------------------')
        ci = input('Enter city: ')
        print('----------------------------------')
        d = input('Enter date in the format yyyy-mm-dd: ')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        while True:
            n = random.randint(1000000, 9999999)
            query1 = "select * from bank_customer where acno=%s"
            c.execute(query1, (n,))
            result = c.fetchone()
            if not result:
                break

        query = "insert into bank_customer values(%s, %s, %s, %s, %s, %s, %s)"
        data = (n, u, p, a, b, ci, d)
        c.execute(query, data)
        mydb.commit()
    except Exception as e:
        print(f"An error occurred while creating an account: {e}")

    print('To create a bank account, a minimum deposit of ₹15000 is required.')
    while True:
        try:
            x = float(input('Enter the money you want to deposit: '))
            now = dt.datetime.now()
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            if x >= 15000:
                q1 = "insert into bank_transactions values(%s, %s)"
                c.execute(q1, (n, x))
                q3 = "insert into bank_report_deposit values(%s,%s,%s,%s)"
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                date_part, time_part = dt_string.split()
                c.execute(q3, (n, date_part, time_part, x))
                print('Your account has been successfully created.')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                break
            else:
                print('Minimum deposit should be ₹15000')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        except ValueError:
            print("Please enter a valid amount.")
    mydb.commit()


def login1():
    while True:
        try:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            user_name = input('Enter your username: ')
            password = input('Enter your password: ')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            query = "select password from bank_customer where username=%s"
            data = (user_name,)
            c.execute(query, data)
            result = c.fetchone()
            if result:
                if result[0] == password:
                    online_banking(user_name)
                    break
                else:
                    print('Wrong password')
            else:
                print('Username not present or wrong username')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                break
        except Exception as e:
            print(f"Login error: {e}")
    mydb.commit()

1


def online_banking(par):
    while True:
        print('Enter 1 to Deposit money')
        print('Enter 2 to Withdraw money')
        print('Enter 3 to View account details')
        print('Enter 4 to Check balance')
        print('Enter 5 to exit')
        print('---------------------------------------')
        ch1 = int(input('Enter your choice: '))
        if ch1 == 1:
            deposit(par)
        elif ch1 == 2:
            withdraw(par)
        elif ch1 == 3:
            details(par)
        elif ch1 == 4:
            balance(par)
        elif ch1 == 5:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
        else:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Wrong choice entered')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def deposit(x):
    print('----------------------------------')
    dep = float(input('Enter the amount to be deposited: '))
    now = dt.datetime.now()
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    q2 = "update_bank_transactions set balance=balance+%s where acno=%s"
    c.execute(q2, (dep, result[0]))
    q3 = "insert into bank_report_deposit values(%s, %s, %s, %s)"
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    a = dt_string.split()
    c.execute(q3, (result[0], a[0], a[1], dep))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Amount has been deposited')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    mydb.commit()


def withdraw(x):
    print('----------------------------------')
    wdrw = float(input('Enter the money you want to withdraw: '))
    now = dt.datetime.now()
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    q2 = "update bank_transactions set balance-balance-%s where acno=%s"
    c.execute(q2, (wdrw, result[0]))
    q3 = "insert into bank_report_withdraw values(%s, %s, %s, %s)"
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    a = dt_string.split()
    c.execute(q3, (result[0], a[0], a[1], wdrw))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Amount has been withdrawn')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    mydb.commit()


def details(x):
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    query1 = "select * from bank_customer where acno=%s"
    c.execute(query1, result)
    result1 = c.fetchone()
    query2 = "select balance from bank_transactions where acno=%s"
    c.execute(query2, result)
    result2 = c.fetchone()
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Your account Details are:-')
    print('----------------------------------')
    print('Account No.:', result1[0])
    print('----------------------------------')
    print('Name:', result1[3])
    print('----------------------------------')
    print('Username:', result1[1])
    print('----------------------------------')
    print('Password:', result1[2])
    print('----------------------------------')
    print('Balance:', result2[0])
    print('----------------------------------')
    print('Mobile No.:', result1[4])
    print('----------------------------------')
    print('City:', result1[5])
    print('----------------------------------')
    print('Date of joining:', result1[6])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def balance(x):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    query = "select balance from bank_transactions where acno=%s"
    c.execute(query, result)
    result1 = c.fetchone()
    print('Your account balance is:', result1[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    mydb.commit()


def login2():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('To delete your account, you have to enter the username and password of your account')
    while True:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        user_name = input('Enter your username: ')
        password = input('Enter your password: ')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        query = "select password from bank_customer where username=%s"
        data = (user_name,)
        c.execute(query, data)
        result = c.fetchone()
        if result:
            if result[0] == password:
                delete(user_name)
                break
            else:
                print('Wrong password')
        else:
            print('Username not present or wrong username')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
    mydb.commit()


def delete(x):
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    query1 = 'delete from bank_customer where acno=%s'
    c.execute(query1, result)
    query2 = "delete from bank_transactions where acno=%s"
    c.execute(query2, result)
    query3 = "delete from bank_report_deposit where acno=%s"
    c.execute(query3, result)
    query4 = "delete from bank_report_withdraw where acno=%s"
    c.execute(query4, result)
    print('Your account has been successfully deleted')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def login3():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('To see the reports, you have to enter the username and password of your account')
    while True:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        user_name = input('Enter your username: ')
        password = input('Enter your password: ')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        qy = "select password from bank_customer where username=%s"
        data = (user_name,)
        c.execute(qy, data)
        result = c.fetchone()
        if result:
            if result[0] == password:
                reports(user_name)
                break
            else:
                print('Wrong password')
        else:
            print('Username not present or wrong username')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
    mydb.commit()


def reports(par):
    while True:
        print('Enter 1 to see reports of deposits')
        print('Enter 2 to see reports of withdrawls')
        print('Enter 3 to exit')
        print('----------------------------------')
        ch2 = int(input('Enter your choice: '))
        if ch2 == 1:
            deposit_report(par)
        elif ch2 == 2:
            withdraw_report(par)
        elif ch2 == 3:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
        else:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Wrong choice entered')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def deposit_report(x):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    q2 = "select date, time, deposit from bank_report_deposit where acno=%s"
    c.execute(q2, result)
    rec = c.fetchall()
    for i in rec:
        print("Date:", i[0], ' ', "Time:", i[1],
              ' ', 'Amount depositted:', i[2])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def withdraw_report(x):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    q1 = 'select acno from bank_customer where username=%s'
    c.execute(q1, (x,))
    result = c.fetchone()
    q2 = "select date, time, withdraw from bank_report_withdraw where acno=%s"
    c.execute(q2, result)
    rec = c.fetchall()
    for i in rec:
        print("Date:", i[0], ' ', "Time:", i[1],
              ' ', 'Amount withdrawn: ', i[2])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def main():
    print('WELCOME TO ABC BANK')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    while True:
        print('Enter 1 for Creating an account')
        print('Enter 2 for Online Banking')
        print('Enter 3 to Delete the account')
        print('Enter 4 to See Reports')
        print('Enter 5 to Exit')
        print('----------------------------------')
        ch = int(input('Enter your choice: '))
        if ch == 1:
            create_account()
        elif ch == 2:
            login1()
        elif ch == 3:
            login2()
        elif ch == 4:
            login3()
        elif ch == 5:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Thank You for choosing ABC Bank')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
        else:
            print('Wrong choice entered')

main()
