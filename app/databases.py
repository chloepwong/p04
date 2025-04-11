# Unbasic Jeans: Chloe Wong, Brian Liu, Raymond Lin, Kishi Wijaya
# SoftDev
# P04:
# 2025-XX-XX
# Time Spent:

import sqlite3, os
from flask import Flask, request, render_template, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Setup
import sqlite3, os, csv
from flask import Flask, request, render_template, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = os.urandom(32)

# database initialization
def init_db():
    """initialize db if none exists"""
    conn = sqlite3.connect('p04.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

# id -> User ID      username -> username        password -> password


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpi (
            date TEXT NOT NULL,
            cpi FLOAT NOT NULL,
            change FLOAT NOT NULL
        )
    ''')


# date -> date   cpi -> consumer price index   change -> change in CPI from previous month


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approval (
            President TEXT NOT NULL,
            date TEXT NOT NULL,
            positive FLOAT NOT NULL,
            negative FLOAT NOT NULL,
            days INT NOT NULL
        )
    ''')


# president -> President  date -> date  positive/negative -> # of (pos/neg) ratings  days -> days since inauguration


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS correlation (
            date TEXT NOT NULL,
            President TEXT NOT NULL,
            cpi FLOAT NOT NULL,
            change FLOAT NOT NULL,
            percent FLOAT NOT NULL
        )
    ''')

# date -> date   president -> President  cpi -> consumer price index   change -> change in CPI from previous month   percent -> percent of positive ratings


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            username TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT NOT NULL
        )
    ''')

# username -> username   id -> COMMENT ID    comment -> comment text


    conn.commit()
    conn.close()

def setup(info):
    date = info.replace("/", "-")
    newdate = date[-4:] + "-" + date[:-5]
    if int(newdate[5]) > 1:
        newdate = newdate[:5] + "0" + newdate[5:]
    if int(newdate[5]) == 1 and newdate[6] == "-":
        newdate = newdate[:5] + "0" + newdate[5:]
    newdate = newdate[:7]
    return newdate


def database_connect():
    if not os.path.exists('p04.db'):
        init_db()
    conn = sqlite3.connect('p04.db')
    return conn

def cpibase():
    if not os.path.exists('p04.db'):
        print("wa")
        try:
            conn = database_connect()
            with open('cpiai_csv.csv') as csvfile:
                readn = list(csv.reader(csvfile))
                cursor = conn.cursor()
                readlen = len(readn)
                count = 0
                for row in readn:
                    count +=1
                    i = count + 1
                    unique = 1
                    while i < readlen:
                        date = row[0]
                        datex = date[:7]
                        ls2 = readn[i]
                        ls2 = ls2[0]
                        ls2 = ls2[:7]
                        if datex == ls2:
                            unique = 0
                            break
                        else:
                            i += 1
                    if unique == 1:
                        cpix = row[1]
                        changex = row[2]
                        cursor.execute('INSERT INTO cpi (date, cpi, change) VALUES (?, ?, ?)', (datex, cpix, changex))
                        print(datex)
                conn.commit()
        except sqlite3.IntegrityError:
            flash('Database Error')
        print ("aprov")
        try:
            conn = database_connect()
            with open('approval_polls.xls') as csvfile:
                readn = list(csv.reader(csvfile))
                cursor = conn.cursor()
                readlen = len(readn)
                count = 0
                for row in readn:
                    count +=1
                    i = count + 1
                    unique = 1
                    while i < readlen:
                        date = row[1]
                        datex = setup(date)
                        ls2 = readn[i]
                        ls2 = ls2[1]
                        ls2 = setup(ls2)
                        print(datex + " vs " + ls2)
                        if datex == ls2:
                            print("oops")
                            unique = 0
                            i = readlen
                        else:
                            i += 1
                    if unique == 1:
                        Presidentx = row[0]
                        positivex = row[2]
                        negativex = row[3]
                        daysx = row[4]
                        print(datex)
                        cursor.execute('INSERT INTO approval (President, date, positive, negative, days) VALUES (?, ?, ?, ?, ?)', (Presidentx, datex, positivex, negativex, daysx))
                conn.commit()
        except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")
#     try:
#             conn = database_connect()
#             with open('approval_polls.xls') as approvalfile and open('cpiai_csv.csv') as cpifile:
#                 readn = csv.reader(approvalfile)
#                 readx = csv.reader(cpifile)
#                 cursor = conn.cursor()
#                 for info in readn:
#                     Presidenta = info[0]
#                     datea = info[1].replace("/", "-")
#                     percenta = info[2]/ (info[2] + info[3])
#                 for data in readn:
#                     dateb = data[0]
#                     cpib = data[1]
#                     changeb = data[2]
#                 if datea = dateb:
#                     cursor.execute('INSERT INTO correlation (date, President, cpi, change, percent) VALUES (?, ?, ?, ?, ?)', (datea, Presidenta, cpib, changeb, percenta))
#                 conn.commit()
#         except sqlite3.IntegrityError:
        
cpibase()


def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # check if fields filled out
    if not username or not password:
        flash('Please fill out all fields.')
        return redirect('/login')

    with sqlite3.connect('p04.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        users_pass = cursor.fetchone()

        if users_pass:
            if users_pass[0] == password:
                session['username'] = username
                flash('Successfully logged in.')
                return redirect('/')
        else:
            flash('Invalid username or password.')
    return redirect('/login')

def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    # check if fields filled out
    if not username or not password or not confirm_pass:
        flash('Please fill out all fields.')

    elif password != confirm_pass:
        flash('Passwords do not match.')

    else:
        try:
            with sqlite3.connect('p04.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash('User registered. Please log in.')
                return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    return redirect('/register')

def logout_user():
    flash('Successfully logged out.')
    session.pop('username',)
    return redirect('/')
