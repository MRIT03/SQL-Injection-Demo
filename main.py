from flask import Flask, render_template, redirect, request, url_for, flash, session
from datetime import timedelta
import sqlite3


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def start():
    return redirect("/login")

def get_db_connection():
    conn = sqlite3.connect('Bank.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def authenticate(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('Bank.db')
    c = conn.cursor()

    # Query for the user by username and password
    query = f"SELECT * FROM Accounts WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    result = c.fetchone()

    # Close the connection
    conn.close()

    # Return True if an entry is found, else False
    return result is not None


@app.route("/login", methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username= request.form['username']
        password = request.form['password']
        try:
            authentication = authenticate(username=username, password=password)
        except Exception as e:
            authentication = False

        if authentication:
           
            session["username"] = username
            
            if username=="admin":
                return redirect("/admin")
            return redirect("/user")
        else:
            msg = "Incorrect username or password"

    return render_template("login.html", msg = msg)


@app.route('/admin')
def admin():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, balance FROM Accounts WHERE username != "admin"').fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@app.route('/user/')
def user():
    if "username" in session:
        username = session["username"]
        conn = get_db_connection()
        user = conn.execute('SELECT balance FROM Accounts WHERE username = ?', (username,)).fetchone()
        conn.close()
        return render_template('user.html', username=username, balance=user['balance'] if user else 0)

    return redirect(url_for("login"))
    

if __name__ == '__main__':
    app.run(debug=True)
