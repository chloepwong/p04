# Unbasic Jeans: Chloe Wong, Brian Liu, Raymond Lin, Kishi Wijaya
# SoftDev
# P04:
# 2025-XX-XX
# Time Spent:


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
        cursor = conn.cursor()
        inserted_dates = set()
        with open('cpiai_csv.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                datex = row[0][:7]
                if datex not in inserted_dates:
                    print(datex)
                    inserted_dates.add(datex)
                    cursor.execute(
                        'INSERT INTO cpi (date, cpi, change) VALUES (?, ?, ?)',
                        (datex, row[1], row[2])
                    )
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')

    try:
        inserted_approval_dates = set()
        with open('approval_polls.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                datex = setup(row[1])
                if datex and datex not in inserted_approval_dates:
                    inserted_approval_dates.add(datex)
                    print(datex)                    
                    cursor.execute(
                        'INSERT INTO approval (President, date, positive, negative, days) VALUES (?, ?, ?, ?, ?)',
                        (row[0], datex, row[2], row[3], row[4])
                    )
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')
    else:
        print("database exists")

        
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
