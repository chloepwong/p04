# Unbasic Jeans: Chloe Wong, Brian Liu, Raymond Lin, Kishi Wijaya
# SoftDev
# P04: 
# 2025-XX-XX
# Time Spent: 

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import databases as db 


db.init_db()

# Secret key/setup
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return render_template('home.html')
    return render_template('home.html', username = session['username'])

# User routing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return db.create_user()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return db.login_user()
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        return db.logout_user()
    return redirect('/')


# Run
if __name__ == "__main__":
    app.debug = True
    app.run()