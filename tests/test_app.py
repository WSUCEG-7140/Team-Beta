from flask import json

from app import app

def test_index():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"<title>IQ Test</title>" in response.data

def test_register_page():
    response = app.test_client().get('/register')
    assert response.status_code == 200

def test_register():
    response = app.test_client().post('/register', data={"username": "New_User", "password": "NewPassword"})
    assert response.status_code == 200

def test_login_page():
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_login():
    response = app.test_client().post('/login', data={"username": "New_User", "password": "NewPassword"})
    assert response.status_code == 302

def test_dashboard():
    response = app.test_client().get('/dashboard')
    assert b"<h1>Welcome to the Dashboard</h1>" in response.data

def test_quiz_page():
    response = app.test_client().get('/quiz')
    assert b"<h1>Quiz</h1>" in response.data

# ... (other test cases remain the same)

# Test for the 'contact_us' route with form submission
def test_contact_us_form_submission():
    """
    Test case for the 'contact_us' method with form submission.
    """
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Test message'
    }
    response = app.test_client().post('/contact_us', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"message" in response.data

    # Decode the JSON response
    response_json = json.loads(response.data)

    # Check the 'message' field in the response
    assert response_json["message"] == "Thank you! We will connect to you shortly."

