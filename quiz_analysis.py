"""@ref R79_0"""

# Importing the required library
import sqlite3   # For working with SQLite database

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect("users.db")   # Connect to the 'users.db' SQLite database

# Function to get the user's quiz performance data from the SQLite database
def get_user_quiz_performance_data(user_id, quiz_id):
    # Connect to the database
    conn = connect_db()   # Call the 'connect_db' function to establish the database connection
    cursor = conn.cursor()   # Create a cursor object to interact with the database

    # Query to fetch the user's quiz performance data
    query = """
    SELECT score, attempt_date FROM quiz_data
    WHERE user_id = ? AND quiz_id = ?
    ORDER BY attempt_date DESC
    """

    # Execute the query and fetch all results
    cursor.execute(query, (user_id, quiz_id))   # Execute the query with provided user_id and quiz_id as parameters
    performance_data = cursor.fetchall()   # Fetch all the results as a list of tuples

    # Close the database connection
    conn.close()   # Close the database connection to free up resources

    # Return the performance data in the required format
    return performance_data   # Return the fetched performance data

# Function to analyze strengths based on the performance data
def analyze_strengths(performance_data):
    # Analyze strengths based on the performance data
    strengths = []
    for score, _ in performance_data:
        if score >= 90:
            strengths.append("Excellent subject knowledge")
        elif 80 <= score < 90:
            strengths.append("Good time management and accuracy")

    return strengths   # Return the list of strengths

# Function to analyze weaknesses based on the performance data
def analyze_weaknesses(performance_data):
    # Analyze weaknesses based on the performance data
    weaknesses = []
    for score, _ in performance_data:
        if score < 80:
            weaknesses.append("Need to improve problem-solving skills and understanding of certain concepts")

    return weaknesses   # Return the list of weaknesses
