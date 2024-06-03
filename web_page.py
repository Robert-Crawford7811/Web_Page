"""Program that makes a webpage"""
from datetime import date
import re
import logging
from flask import Flask, render_template,  request, redirect, url_for, session

# Calls the imported flask function and sets to render the web pages in the "template" form
app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

#User Data and variables being used
users = {'username': 'password'}
#Password Complexity
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'

#Load Common Password File
COMMON_PASSWORDS = 'CommonPassword.txt'
def load_common_passwords():
    '''Function that loads the "common passwords file'''
    with open(COMMON_PASSWORDS, encoding="utf-8" 'r') as file:
        return set(file.read().splitlines())

def failed_logins(ip_address):
    '''Functions that logs failed login attempts'''
    logging.basicConfig(filename='failed_login_attempts.log', level=logging.INFO)
    logging.info("Failed login attempt from IP address: %s", format(ip_address))

# Defining the website routes
@app.route('/')
# Sets up registration page for the site
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Function that renders the registration page'''
    if request.method == 'POST':
        # Establishes the username and password variables to be inputted into the form
        username = request.form['username']
        password = request.form['password']
        if username in users:
            # Refreshes the page and prints a message when username already exists.
            return render_template('register.html', message='Username already exists.')
        if not re.match(PASSWORD_REGEX, password):
            # Refreshes the page and prints a message when password isn't complex enough
            return render_template('register.html', message='Password complexity not met.')

        users[username] = password
        # Redirects to the login screen
        return redirect(url_for('login'))

    return render_template('register.html',date=date.today())
# Sets up login page for the site
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Function that renders the login page'''
    if request.method == 'POST':
        # Establishes the username and password variables to be inputted into the form
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            # Redirects to the home page screen
            return redirect(url_for('home_page'))
        # Refreshes the page and prints a message when username already exists.
        failed_logins(request.remote_addr)
        return render_template('login.html', message='Invalid credentials.')
    #Renders the login page
    return render_template('login.html',date=date.today())

def common_password(new_password):
    '''Function that compares password to text file of common password'''
    common_passwords = load_common_passwords()
    return new_password in common_passwords

# Sets up password update page for the site
@app.route('/password_update', methods=['GET', 'POST'])
def password_update():
    '''Function that renders the password update page'''
    if request.method == 'POST':
        # Establishes the current and new password variables to be inputted into the form
        new_password = request.form['new_password']
        if not re.match(PASSWORD_REGEX, new_password):
            # Refreshes the page and prints a message when password isn't complex enough
            return render_template('password_update.html', message='Password complexity not met.')
        if common_password(new_password):
            # Refreshes the page and prints a message when password is too common
            return render_template('password_update.html', message='New Password is too common.')

    #Renders password update page
    return render_template('password_update.html', date=date.today())

@app.route('/home_page.html')
#Defines home page route
def home_page():
    #Render Home Page
    '''Function that renders the home page of the website'''
    return render_template('home_page.html',date=date.today())

#Defines second page route
@app.route('/page2.html')
def page2():
    # Render second web page
    '''Function that renders the second page of the website'''
    return render_template('page2.html',date=date.today())

#Defines third page route
@app.route('/page3.html')
def page3():
    # Render third web page
    '''Function that renders the third page of the website'''
    return render_template('page3.html',date=date.today())

if __name__ == "__main__":
    app.run(debug=True)
