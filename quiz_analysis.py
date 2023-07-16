import sqlite3

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect("users.db")

# Function to get the user's quiz performance data from the SQLite database
def get_user_quiz_performance_data(user_id, quiz_id):
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Query to fetch the user's quiz performance data
    query = """
    SELECT score, attempt_date FROM quiz_data
    WHERE user_id = ? AND quiz_id = ?
    ORDER BY attempt_date DESC
    """

    # Execute the query and fetch all results
    cursor.execute(query, (user_id, quiz_id))
    performance_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return the performance data in the required format
    return performance_data

# Function to analyze strengths based on the performance data
def analyze_strengths(performance_data):
    # Analyze strengths based on the performance data
    strengths = []
    for score, _ in performance_data:
        if score >= 90:
            strengths.append("Excellent subject knowledge")
        elif 80 <= score < 90:
            strengths.append("Good time management and accuracy")

    return strengths

# Function to analyze weaknesses based on the performance data
def analyze_weaknesses(performance_data):
    # Analyze weaknesses based on the performance data
    weaknesses = []
    for score, _ in performance_data:
        if score < 80:
            weaknesses.append("Need to improve problem-solving skills and understanding of certain concepts")

    return weaknesses
