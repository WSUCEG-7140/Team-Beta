import requests
import csv

def fetch_iq_questions():
    # Get the list of open source resources that contain IQ questions.
    resources = [
        "https://www.iqtest.com/questions",
        "https://www.mensa.org/iq/questions",
        "https://www.freeiqtest.net/questions",
    ]

    # Initialize a CSV file to store the IQ questions.
    csvfile = open("iq_questions.csv", "w")
    writer = csv.writer(csvfile, delimiter=",")

    # Fetch the IQ questions from each resource.
    for resource in resources:
        response = requests.get(resource)
        if response.status_code == 200:
            # The response is successful.
            content = response.content.decode("utf-8")
            questions = content.split("\n")
            for question in questions:
                # Write the question to the CSV file.
                writer.writerow([question])
        else:
            # The response is not successful.
            print(f"Failed to fetch IQ questions from {resource}")

if __name__ == "__main__":
    fetch_iq_questions()
