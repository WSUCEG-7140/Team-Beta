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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #created a database which stores and registers our id and password 
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
    """
@brief The code defines a route for the root URL ("/") of the web application. When a user accesses the root URL, the function index() is triggered. The function will render an HTML template named "index.html" and return it to the user's browser
@pre The code appears to be written using Python and the Flask web framework.
There is a route decorator @app.route('/') indicating that this function will handle requests to the root URL of the application.
The code seems to rely on Flask's render_template function to render an HTML template.
@post The Flask application will be able to handle incoming requests to the root URL. When a user accesses the root URL, the index() function will be invoked. The function will generate a response by rendering the "index.html" template. This HTML content will be sent back to the user's browser.
@return The function index() does not have an explicit return statement, but it implicitly returns the result of render_template('index.html'), which is an HTML content generated from the "index.html" template.
"""
    return render_template('index.html')

# Route for user registration, handles registration form submission
@app.route('/register', methods=['GET', 'POST'])
def register():
     """
    @brief This function contains the new user registeration process and another route for user  login
    @pre the register function is the HTTP request page which should be Posted , which indicates
     has to submit the registration form.If the request method is not submitted , the function 
     will not proceed with user registration process and will render the 'register.html' template.
    @post when the 'register' function is succesfull, a new user is added to the database 
     and the user will be redirected to the login page.
""" 
    # Handling the POST request when the user submits the registration form
     if request.method == 'POST':
         # Retrieving username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

        # Insert the new user into the database
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
    """
    @brief the 'login ' function handles user login. it checks whether the request method is  
    'POST', indicating that the user has submitted the login details .
    @pre When the HTTP request method must be 'POST' , indicating that the user has submitted 
    the user has submitted login details .
    Users data 'Password' should be stored database based on the user's 'username'.
    @post If the login is successful (i.e., a valid user with the correct password is found in                     database), the user's username is stored in the session.
    If the login is unsuccessful (invalid username or password), an error message is displayed on the login page.
    @return The return value of the login function depends on whether the login is successful or not. If the login is successful, the function performs a redirection to the 'dashboard' page using redirect(url_for('dashboard')). If the      	login is unsuccessful (invalid username or password), the function renders the 'login.html' template with an error message. 
    """
    # Handling the POST request when the user submits the login form
    if request.method == 'POST':
        # Retrieving username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Successful login
            # Store the username in the session
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
     """
    @brief 'dashborad' funciton si responsible for displaying the dashboard page to authorized users . it retrives the username , which should have been stored during successful login.
    @pre The user should be authenticated and logged in. The 'username' must be stored in the session during the login process. If the ' username ' is not found in the session (i.e., the user is not logged in), the dashboard may still            	be displayed, but it might not show personalized content.
   @post The postconditions for the 'dashboard' function are that it renders the 'dashboard.html' template with the appropriate 'username' passed as a context variable.The template 'dashboard.html' can then use the username variable to  	display personalized content for the authenticated user.
     """
    # Retrieve the username from the session
     username = session.get('username')
    # Rendering the dashboard page with the username passed as a parameter
    
     return render_template('dashboard.html', username=username)



def calculate_score(predicted_answers):
    """
        @brief The 'calculate_score' function is designed to calculate a score based on a list of predicted answers. It iterates through the list of answers, checks if each answer is numeric, and accumulates the numeric answers to         calculate the final score.
        @pre The predicted_answers parameter should be a list of strings containing predicted answers.
        @post The 'calculate_score' function returns the calculated score as a floating-point number. 
        @return The function returns the calculated score as a floating-point number.
 	"""
    score = 0
    for answer in predicted_answers:
        if not answer.isdigit():
            # Handle non-numeric values
            score += 0  # Assign a score of 0 for non-numeric answers
        else:
            # Convert the answer to a float and add it to the score
            score += float(answer)
    return score

def generate_random_score():
    """
        @brief The generate_random_score function generates a random score between 41 and 100 (inclusive).
        @post The function returns a randomly generated score as an integer.
        @return The function returns a randomly generated score as an integer.
	"""
    return random.randint(41, 100)

def create_bar_chart_data(scores):
    """
        @brief The create_bar_chart_data function takes a list of scores as input and converts it into a format suitable for a bar chart. It creates a list of dictionaries, each containing a 'label' and 'value', where the 'label' is  'Score', and the 'value' corresponds to each score in the input list.
        @pre The scores parameter should be a list of scores (numeric values).
        @post The function returns a list of dictionaries with 'label' and 'value' keys.
        @return The function returns the processed data as a list of dictionaries.
	"""
    data = [{'label': 'Score', 'value': score} for score in scores]
    return data

def create_pie_chart_data(scores):
    """
        @brief The 'create_pie_chart_data' function takes a list of scores as input and converts it into a format suitable for a pie chart. It creates a list of dictionaries, each containing a 'label' with the format 'Score i+1' (where     is the index) and 'value' corresponding to each score in the input list.
        @pre The 'scores' parameter should be a list of scores (numeric values) .
        @post The function returns a list of dictionaries with 'label' and 'value' keys.
        @return The function returns the processed data as a list of dictionaries.
	"""
    data = [{'label': f'Score {i+1}', 'value': score} for i, score in enumerate(scores)]
    return data

def create_line_chart_data(scores):
    """
        @brief The 'create_line_chart_data' function takes a list of scores as input and converts it into a format suitable for a line chart. It creates a list of dictionaries, each containing an 'x' and 'y' value, where 'x' is the index of the score in the input list plus 1, and 'y' corresponds to each score in the input list.
        @pre The scores parameter should be a list of scores (numeric values).
        @post The function returns a list of dictionaries with 'x' and 'y' keys
	"""
    data = [{'x': i+1, 'y': score} for i, score in enumerate(scores)]
    return data

# Route for the quiz, handles quiz form submission
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
@brief The function provided, 'quiz()', is a route handler for the URL path '/quiz'. It serves a quiz consisting of 10 random questions with multiple-choice options to the user. The user can submit their answers via a form on the page. The function handles both GET and POST requests. For POST requests, it evaluates the submitted answers, calculates the user's score based on the correctness of their answers, and stores the score in the session. Then, it redirects the user to the 'result' page to display their quiz result. For GET requests, the function displays the quiz page with randomly selected questions and their multiple-choice options. It also displays any previously selected answers stored in the session, if available.
@pre The 'result' route handler should be defined to handle the redirect after quiz submission.A trained machine learning model stored in 'random_forest_model.pkl' should be available for use.The 'calculate_score()' function should be defined to evaluate the user's answers and calculate the score. A CSV file named 'quiz.csv' should exist, containing quiz questions, options, and correct answers.
@return For POST requests, the function redirects the user to the 'result' page using 'redirect(url_for('result'))' after evaluating their quiz answers.For GET requests, the function returns the HTML content of the 'quiz.html' template, rendering the quiz page with the selected questions and any previously selected answers to be displayed. The 'questions' and 'selected_answers' variables will be used to populate the quiz page.
@post For POST requests:
The selected answers are retrieved from the form and stored in the session.
The trained machine learning model is loaded from 'random_forest_model.pkl'.
The selected answers are transformed into a Bag-of-Words representation using 'vectorizer'.
The trained model predicts the correct answers for the selected questions.
The predicted answers are evaluated, and the user's score is calculated using 'calculate_score()' function.
The calculated score is stored in the session.
The user is redirected to the 'result' page to view their quiz score.
For GET requests:
Any previously selected answers are retrieved from the session.
The quiz questions, options, and correct answers are read from 'quiz.csv'.
10 random questions are selected from the pool of questions to be displayed on the quiz page.
The quiz page is rendered with the selected questions and any previously selected answers.
"""
    if request.method == 'POST':
        # Retrieve the selected answers from the form
        selected_answers = []
        for i in range(1, 11):
            answer = request.form.get(f'question_{i}')
            selected_answers.append(answer)

        # Store the selected answers in the session
        session['selected_answers'] = selected_answers

        try:
            # Load the trained model from the .pkl file
            with open('random_forest_model.pkl', 'rb') as f:
                model = pickle.load(f)

            # Transform the selected answers using the CountVectorizer
            selected_answers_bow = vectorizer.transform(selected_answers)

            # Perform predictions using the trained model
            predicted_answers = model.predict(selected_answers_bow)

            # Evaluate the answers and calculate the score
            score = calculate_score(predicted_answers)

        except:
            # Fall back to comparing selected answers with CSV file's correct answers
            # Read the correct answers from the CSV file
            correct_answers = []
            with open('quiz.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    correct_answers.append(row['Answer'])

            # Evaluate the answers and calculate the score
            score = 0
            for selected, correct in zip(selected_answers, correct_answers):
                if selected == correct:
                    score += 1

        # Store the score in the session
        session['score'] = score

        # Redirect to the result page
        return redirect(url_for('result'))

    # Check if there are any previously selected answers in the session
    selected_answers = session.get('selected_answers', [])

    # Read the quiz questions from the CSV file
    questions = []
    with open('quiz.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            options = [value for key, value in row.items() if key != 'Answer']
            question = {
                'question': row['Question'],
                'options': options
            }
            questions.append(question)

    # Select 10 random questions
    selected_questions = random.sample(questions, 10)

    return render_template('quiz.html', questions=selected_questions, selected_answers=selected_answers)


def calculate_percentile_rank(score, scores):
    """
@brief The function provides, 'calculate_percentile_rank()', calculates the percentile rank of a given 'score' within a list of 'scores'. The percentile rank represents the percentage of scores in the list that are lower than or equal to the given score.
@pre The function expects two parameters:
'score': The score for which the percentile rank needs to be calculated.
'scores': A list of numerical scores, against which the percentile rank will be calculated.
Both 'score' and 'scores' should be numeric values (int or float).
@return The function returns the calculated percentile rank as a floating-point number representing the percentage of scores in the 'scores' list that are lower than or equal to the given 'score'. The value returned will be between 0.0 and 100.0 (inclusive).
@post The function sorts the 'scores' list in descending order.It then finds the index of the 'score' in the sorted list, which represents its position within the list of scores.The percentile rank is calculated as the percentage of scores in the list that are lower than or equal to the given 'score'.
"""
    # Sort the scores in descending order
    sorted_scores = sorted(scores, reverse=True)

    # Find the index of the current score in the sorted list
    index = sorted_scores.index(score)

    # Calculate the percentile rank as a percentage
    percentile_rank = (index / len(sorted_scores)) * 100

    return percentile_rank


def get_interpretation(score):
    """
@brief The function provides, 'get_interpretation()', is responsible for providing an interpretation based on a given 'score'. It categorizes the input score into different levels of performance and returns an interpretation message accordingly.
@pre The function expects a numerical 'score' as an input parameter, representing the performance of a user or entity.
The score should be a numeric value (int or float).
@return The function returns the interpretation message as a string based on the provided 'score'. The interpretation message will describe the performance level associated with the score.
@post The function determines the performance level based on the given score and provides an interpretation.
The returned interpretation message will be one of the following:
"Highly gifted" if the score is greater than or equal to 120.
"Above average" if the score is greater than or equal to 90 but less than 120.
"Average" if the score is greater than or equal to 70 but less than 90.
"Below average" if the score is less than 70.
"""
    # Define your logic to provide an interpretation based on the score
    if score >= 120:
        interpretation = "Highly gifted"
    elif score >= 90:
        interpretation = "Above average"
    elif score >= 70:
        interpretation = "Average"
    else:
        interpretation = "Below average"

    return interpretation




@app.route('/result')
def result():
    """
@brief This function is a route handler for the URL path '/result'. It is designed to display the results of a user's score. The function retrieves the user's score from the session. If the score is not available (equal to 0), it generates a random score using the 'generate_random_score()' function. The function then retrieves a list of all scores from the session, appends the current score to the list, and updates the session with the new scores. It calculates the percentile rank of the current score based on all the scores stored in the session. Additionally, the function obtains an interpretation for the score using the 'get_interpretation()' function. It creates data for three types of charts: bar chart, pie chart, and line chart, using respective functions: 'create_bar_chart_data()', 'create_pie_chart_data()', and 'create_line_chart_data()'. The function then renders the 'result.html' template, passing all the relevant data to be displayed on the page.
@pre The 'generate_random_score()', 'calculate_percentile_rank()', 'get_interpretation()', 'create_bar_chart_data()', 'create_pie_chart_data()', and 'create_line_chart_data()' functions should be defined and available.
@return The function returns the output of the 'render_template' function, which is the HTML content of the 'result.html' template. The template will display the following variables:
'score': The user's current score.
'percentile_rank': The percentile rank of the user's current score.
'interpretation': The interpretation of the user's current score.
'bar_chart_data': Data for a bar chart representing the user's scores.
'pie_chart_data': Data for a pie chart representing the user's scores.
'line_chart_data': Data for a line chart representing the user's scores.
@post The function retrieves or generates a score and stores it in the session.The session will be updated with the new score appended to the list of scores.The percentile rank for the current score will be calculated based on all the scores stored in the session.An interpretation for the current score will be obtained.Data for three types of charts (bar chart, pie chart, line chart) will be created based on the scores stored in the session.
"""
    score = session.get('score')
    if score == 0:
        score = generate_random_score()

    # Retrieve all scores from the session
    scores = session.get('scores', [])
    # Append the current score
    scores.append(score)
    # Update the scores in the session
    session['scores'] = scores

    # Calculate percentile rank
    percentile_rank = calculate_percentile_rank(score, scores)

    # Get interpretation
    interpretation = get_interpretation(score)

    # Create chart data
    bar_chart_data = create_bar_chart_data(scores)
    pie_chart_data = create_pie_chart_data(scores)
    line_chart_data = create_line_chart_data(scores)

    return render_template('result.html', score=score, percentile_rank=percentile_rank,
                        interpretation=interpretation, bar_chart_data=bar_chart_data,
                        pie_chart_data=pie_chart_data, line_chart_data=line_chart_data)

    
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    """
@brief updates a route handler for the URL path '/contact_us'.
This function renders a template called 'contact_us.html', passing the 'message' variable to be displayed on the page.It accepts both GET and POST requests. If a POST request is received, the function processes the form data (name, email, and message) and then prints the form data to the consoleIt also sets a 'message' variable to "Thank you! We will connect to you shortly." 
@pre The 'Flask' library should be imported and the 'app' object should be instantiated. The 'contact_us.html' template should exist and be properly formatted with a placeholder to display the 'message' variable.
@return The output of the 'render_template' function, which is the HTML content of the 'contact_us.html' template with the 'message' variable properly replaced.
@post The GET request is made to '/contact_us', the 'contact_us.html' template will be rendered with the 'message' variable set to None (no message will be displayed initially).
The POST request is made to '/contact_us' with form data containing 'name', 'email', and 'message', the function will process the data and print it to the console. It will render 'contact_us.html' with the 'message' variable set to "Thank you! We will connect to you shortly." The updated message will be displayed on the page.
"""
    message = None  # Initialize the message variable

    if request.method == 'POST':
        # Process the form submission (you can handle form data here)
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Here you can handle the form data as needed (e.g., send an email, save to database, etc.)
        # For this example, we will simply print the form data
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Set the message to be displayed on the page
        message = "Thank you! We will connect to you shortly."

    return render_template('contact_us.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
