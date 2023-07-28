"""@ref R79_0"""

# Importing the required library
import sqlite3   # For working with SQLite database
#from contracts import contract, pre, post
# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect("users.db")   # Connect to the 'users.db' SQLite database
"""
   @brief The function is responsible for establishing a connection to an SQLite database named "users.db" that stores user information, such as usernames and passwords.
   @pre:The function assumes that the SQLite database file named "users.db" exists in the current working directory.The SQLite library must be imported and available for establishing the         
   database connection.
   @post:After successful execution of the function, a connection to the "users.db" database is established.The returned connection object can be used to perform various            
   database operations, such as querying or inserting data.
   @return:The function returns an SQLite database connection object that represents the connection to the "users.db" database.
   The connection object can be utilized in other parts of the code to interact with the database, such as executing SQL queries or committing transactions.
"""

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

"""
   @brief:   The function fetches quiz performance data for a user and quiz from the "quiz_data" table. It takes user_id and quiz_id as inputs and returns a list of score-date tuples,                                                                     
   @pre:The 'sqlite3' module must be imported to enable database connectivity.The database connection must be established using the 'connect_db' function before calling this          function.sorted by date in descending order.
   @post: The function will execute a SQL query to fetch quiz performance data for the specified user_id and quiz_id from the "quiz_data" table. The performance data is ordered by the   attempt date in descending order, and the database connection is closed after retrieval.
   @return: The function returns a list of tuples containing the quiz performance data for the specified user and quiz. Each tuple in the list consists of two elements: the quiz score and the attempt date. The list is ordered based on the attempt date, with the most recent attempts appearing first.

"""





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
"""
   @brief The function takes performance data as input and analyzes strengths based on the provided scores. It identifies strengths based on score ranges and generates a list of corresponding strength descriptions. The function returns a list of strengths based on the analysis.
@pre The performance_data parameter should be a list of tuples, where each tuple contains a numerical score (integer or float) as its first element, and an optional additional element that is not used in this function (denoted by _).
@post:The function will analyze the performance data and generate a list of strengths based on the score ranges defined in the function.
The strengths list will only contain descriptions for scores that fall within specific ranges (e.g., excellent subject knowledge for scores >= 90 and good time management and accuracy for scores between 80 and 89).Scores that do not fall within any specified range will not have corresponding strengths included in the output.
@return:
The function returns a list of strengths identified from the provided performance data. Each element in the list represents a specific strength associated with a corresponding score range.

"""


# Function to analyze weaknesses based on the performance data
def analyze_weaknesses(performance_data):
    # Analyze weaknesses based on the performance data
    weaknesses = []
    for score, _ in performance_data:
        if score < 80:
            weaknesses.append("Need to improve problem-solving skills and understanding of certain concepts")

    return weaknesses   # Return the list of weaknesses

"""
   @brief: The function analyzes weaknesses based on the quiz performance data, taking performance_data as input (a list of score-date tuples). It identifies weaknesses  for scores below   80 and returns a list of weakness descriptions associated with the user's performance.
   @pre: The performance_data parameter should be a list of tuples containing quiz scores and corresponding attempt dates. 
   @post: The function analyzes quiz scores in performance_data to identify weaknesses based on predefined criteria. Weaknesses are stored in a list called weaknesses
   @return: The function returns a list of weaknesses associated with the user's quiz performance. Each weakness is represented as a string describing the area of improvement based on the quiz score.

"""
