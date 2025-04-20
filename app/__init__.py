# Unbasic Jeans: Chloe Wong, Brian Liu, Raymond Lin, Kishi Wijaya
# SoftDev
# P04: 
# 2025-4-21
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

# Write discussion comment
@app.route("/write", methods=['GET', 'POST'])
def write():
    if session.get("username") == None:
        return redirect(url_for("login"))
    if request.method=="POST":
        comment = request.form.get("comment")
        commentid = db.addComment(session.get("username"), comment)[0]
        return redirect("/discussion")
    return render_template("write.html", username = session.get("username"))

# View full discussion
@app.route("/discussion")
def discussion():
    print(session)
    if session.get("username") == None:
        return redirect(url_for("login"))
    coms = db.getAllComments()
    comments = []
    #print(coms)
    for i in range(len(coms)):
        sub = coms[i][0]
        comments.append(sub)
    print(comments)
    username = session['username']
    return render_template("discussion.html", comments=comments, username=username)

from flask import request

@app.route("/graphs")
def graphs():
    conn = db.database_connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, cpi FROM cpi WHERE date >= '2000'")
    cpi_data = cursor.fetchall()
    
    cursor.execute("SELECT date, positive, negative FROM approval WHERE date >= '2000'")
    approval_data = cursor.fetchall()
    
    conn.close()
    
    dates = []
    cpi_values = []
    for row in cpi_data:
        dates.append(row[0])
        cpi_values.append(row[1])

    ratings = {}
    for row in approval_data:
        date = row[0]
        pos = float(row[1])
        neg = float(row[2])
        approval = (pos / (pos + neg)) * 100
        ratings[date] = approval
    
    approval_values = []
    for date in dates:
        value = ratings.get(date)
        approval_values.append(value)

    return render_template("graphs.html", dates=dates, cpi_values=cpi_values, approval_values=approval_values, username = session.get("username"))

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()