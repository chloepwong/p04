# 
# Unbasic Jeans
# SoftDev
# P04: 
# 

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from databases import 


init_db()

# Secret key/setup
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    #print("\n\nget_all_favorites:",get_all_favorites())
    if 'username' not in session:
        return render_template('home.html')
    return render_template('home.html', username = session['username'])

# User routing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return create_user()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return login_user()
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        return logout_user()
    return redirect('/')


# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
