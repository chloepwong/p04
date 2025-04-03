 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
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

def database_connect():
    if not os.path.exists('p04.db'):
        init_db()
    conn = sqlite3.connect('p04.db')
    return conn


#Flower
def cpibase():
    if not os.path.exists('p04.db'):
        print("wa")
        try:
            conn = database_connect()
            with open('cpiai_csv.csv') as csvfile:
                readn = csv.reader(csvfile)
                cursor = conn.cursor()
                for info in readn:
                    datex = info[0]
                    cpix = info[1]
                    changex = info[2]
                    cursor.execute('INSERT INTO cpi (date, cpi, change) VALUES (?, ?, ?)', (datex, cpix, changex))
                conn.commit()
        except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")

cpibase()

#Garden
# def garden(user):
#     try:
#         conn = database_connect()
#         for r in range(6):
#             for c in range(6):
#                 cursor = conn.cursor()
#                 cursor.execute('INSERT INTO garden (user, flower_type, days_watered, days_since_watered, max_growth) VALUES (?, ?, ?, ?, ?)', (user, "none", 0, 0, 0))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         flash('Database Error')
# 
# def get_garden(user):
#     try:
#         conn = database_connect()
#         cursor = conn.cursor()
#         result = cursor.execute('SELECT * FROM garden WHERE user = ?', (user)).fetchall()
#     except sqlite3.IntegrityError:
#         flash('Database Error')
# 
# def garden_add(user, ID, flower_type):
#     try:
#         conn = database_connect()
#         cursor = conn.cursor()
#         max_growth = cursor.execute('SELECT max_growth FROM flower_base WHERE flower_type = ?', (flower_type)).fetchone()
#         cursor.execute('UPDATE garden SET flower_type = ? AND max_growth = ? WHERE user = ? AND id = ?', (flower_type, max_growth, user, ID))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         print('Database Error')
# 
# def garden_water(user, ID):
#     try:
#         conn = database_connect()
#         cursor = conn.cursor()
#         days_watered = cursor.execute('SELECT days_watered FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
#         days_since_watered = cursor.execute('SELECT days_since_watered FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
#         max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
#         if(days_since_watered != 0 and days_watered != max_growth):
#             cursor.execute('UPDATE garden SET days_watered = ? WHERE user = ? AND id = ?', (days_watered + 1, user, ID))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         print('Database Error')
# 
# def garden_pick(user, id):
#     try:
#         conn = database_connect()
#         cursor = conn.cursor()
#         flower_type = cursor.execute('SELECT flower_type FROM garden WHERE user = ? AND id = ?', (user, id)).fetchone()
#         max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, id)).fetchone()
#         cursor.execute('UPDATE garden SET flower_type = ? AND days_watered = ? AND days_since_watered = ? AND max_growth = ? WHERE user = ? AND id = ?', ("none", 0, 0, 0, user, id))
#         conn.commit()
#         profile(user, flower_type, max_growth)
#     except sqlite3.IntegrityError:
#         print('Database Error')


User
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    if not username or not password or not confirm_pass:
        flash('fill all fields')
    elif password != confirm_pass:
        flash('passwords dont match')
    else:
        try:
            with sqlite3.connect('p04.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
                conn.commit()
                flash('registered')
        except sqlite3.IntegrityError:
            flash('username already exists')
    return redirect('/login')

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('fill all fields')
        return redirect('/login')
    else:
        with sqlite3.connect('p04.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            user_pass = cursor.fetchone()

            if user_pass:
                if user_pass[0] == password:
                    session['username'] = username
                    flash('logged in')
                    return redirect('/')
            else:
                flash('invalid credentials')
    return redirect('/login')

def logout_user():
    session.pop('username',)
    flash('logged out')
    return redirect('/login')