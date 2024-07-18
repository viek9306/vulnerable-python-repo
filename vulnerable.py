import sqlite3
import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"

# Insecure Protocol (HTTP)
@app.route('/fetch_data')
def fetch_data():
    url = request.args.get('url')
    command = f"curl {url}"  # Using HTTP protocol without SSL
    result = subprocess.check_output(command, shell=True)
    return result

# SQL Injection Vulnerability
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable SQL query (SQL Injection)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials!"
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Cross-Site Scripting (XSS)
@app.route('/search')
def search():
    query = request.args.get('query')
    
    # Vulnerable to XSS
    return render_template_string(f"Search results for: {query}")

if __name__ == '__main__':
    # Initial setup to create a vulnerable database
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE users (username TEXT, password TEXT)')
        cursor.execute(f"INSERT INTO users VALUES ('{USERNAME}', '{PASSWORD}')")
        conn.commit()
        conn.close()
    
    app.run(debug=True)
