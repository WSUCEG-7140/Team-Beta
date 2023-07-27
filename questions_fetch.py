"""@ref R23_0"""

# Importing required libraries
import requests  # For making HTTP requests
import csv       # For working with CSV files

# Function to fetch IQ questions from open source resources and store them in a CSV file
def fetch_iq_questions():
    # List of URLs of open source resources that contain IQ questions
    resources = [
        "https://www.iqtest.com/questions",
        "https://www.mensa.org/iq/questions",
        "https://www.freeiqtest.net/questions",
    ]

    # Initialize a CSV file to store the IQ questions
    csvfile = open("iq_questions.csv", "w")   # Open the CSV file in write mode
    writer = csv.writer(csvfile, delimiter=",")   # Create a CSV writer with comma as the delimiter

    # Fetch the IQ questions from each resource
    for resource in resources:
        response = requests.get(resource)   # Send an HTTP GET request to the resource
        if response.status_code == 200:
            # The response is successful (status code 200)
            content = response.content.decode("utf-8")   # Decode the response content to a string
            questions = content.split("\n")   # Split the content by newline to get individual questions
            for question in questions:
                # Write the question to the CSV file as a new row
                writer.writerow([question])
        else:
            # The response is not successful (status code other than 200)
            print(f"Failed to fetch IQ questions from {resource}")

# Entry point of the script
if __name__ == "__main__":
    fetch_iq_questions()   # Call the function to fetch IQ questions
