"""@ref R104_0"""

# Importing required modules from Flask and other libraries
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import csv
import random
import vectorize as vectorizer
import pickle
import json

# Initializing the Flask app
app = Flask(__name__)

# Configuring the SQLite database URI for user registration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Setting the secret key for Flask session management
app.secret_key = 'your_secret_key'

# Defining the User model for database storage
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Route for the homepage, renders 'index.html'
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration, handles registration form submission
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handling the POST request when the user submits the registration form
    if request.method == 'POST':
        # Retrieving username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Checking if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

        # Inserting the new user into the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Redirecting to the login page after successful registration
        return redirect(url_for('login'))

    # Rendering the registration form for GET requests
    return render_template('register.html')

# Route for user login, handles login form submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handling the POST request when the user submits the login form
    if request.method == 'POST':
        # Retrieving username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Retrieving the user from the database based on the provided username
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Successful login
            # Storing the username in the session
            session['username'] = username

            # Redirecting to the dashboard page after successful login
            return redirect(url_for('dashboard'))

        # Handling the case of invalid username or password
        error = 'Invalid username or password.'
        return render_template('login.html', error=error)

    # Rendering the login form for GET requests
    return render_template('login.html')

# Route for the dashboard, displays user-specific content
@app.route('/dashboard')
def dashboard():
    # Retrieving the username from the session
    username = session.get('username')

    # Rendering the dashboard page with the username passed as a parameter
    return render_template('dashboard.html', username=username)

# Functions to calculate score and generate random score for the quiz
# (code for these functions is missing but presumably handles scoring logic)

# Route for the quiz, handles quiz form submission
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # (Quiz handling logic is present, not fully commented)

# Functions to calculate percentile rank, generate interpretation, and create chart data for the quiz result
# (code for these functions is missing but presumably handles scoring logic)

# Route for displaying the quiz result
@app.route('/result')
def result():
    # (Quiz result handling logic is present, not fully commented)

# Route for the contact us page, handles contact form submission
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    # Handling the POST request when the user submits the contact form
    if request.method == 'POST':
        # Processing the form submission (logic for handling form data is missing)
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Printing the form data (in this example)
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Setting the message to be displayed on the page
        message = "Thank you! We will connect to you shortly."

    # Rendering the contact us page with the message passed as a parameter
    return render_template('contact_us.html', message=message)

# Starting the Flask app and running it in debug mode
if __name__ == '__main__':
    app.run(debug=True)
