from flask import Flask, render_template, request, redirect, url_for, session

from flask_sqlalchemy import SQLAlchemy
import csv
import random
import vectorize as vectorizer
import pickle
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #created a database which stores and registers our id and password 
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Successful login
            # Store the username in the session
            session['username'] = username

            return redirect(url_for('dashboard'))

        error = 'Invalid username or password.'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Retrieve the username from the session
    username = session.get('username')

    return render_template('dashboard.html', username=username)



def calculate_score(predicted_answers):
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
    return random.randint(41, 100)

def create_bar_chart_data(scores):
    data = [{'label': 'Score', 'value': score} for score in scores]
    return data

def create_pie_chart_data(scores):
    data = [{'label': f'Score {i+1}', 'value': score} for i, score in enumerate(scores)]
    return data

def create_line_chart_data(scores):
    data = [{'x': i+1, 'y': score} for i, score in enumerate(scores)]
    return data

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
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
    # Sort the scores in descending order
    sorted_scores = sorted(scores, reverse=True)

    # Find the index of the current score in the sorted list
    index = sorted_scores.index(score)

    # Calculate the percentile rank as a percentage
    percentile_rank = (index / len(sorted_scores)) * 100

    return percentile_rank


def get_interpretation(score):
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
