from app import app
#from contracts import contract,pre,post
# Test for the main index page
def test_index():
    """
        Test case for the 'test_index' method of the 'index' class.
        """
    response = app.test_client().get('/')
    assert response.status_code == 200   # Assert that the response status code is 200 (OK)
    assert b"<title>IQ Test</title>" in response.data   # Assert that the response contains the specified title

# Test for the 'register' page
def test_register_page():
    """
        Test case for the 'test_register_page' method of the 'register page' class.
        """
    response = app.test_client().get('/register')       
    assert response.status_code == 200   # Assert that the response status code is 200 (OK)

# Test for the 'register' route with POST data
def test_register():
    """
        Test case for the 'test_register' method of the 'register' class.
        """
    response = app.test_client().post('/register', data={"username": "New_User", "password": "NewPassword"})
    assert response.status_code == 200   # Assert that the response status code is 200 (OK)

# Test for the 'login' page
def test_login_page():
    """
        Test case for the 'test_login_page' method of the 'login page' class.
        """
    response = app.test_client().get('/login')
    assert response.status_code == 200   # Assert that the response status code is 200 (OK)

# Test for the 'login' route with POST data
def test_login():
    """
        Test case for the 'test_login' method of the 'test_login' class.
        """
    response = app.test_client().post('/login', data={"username": "New_User", "password": "NewPassword"})
    assert response.status_code == 302   # Assert that the response status code is 302 (Redirect)

# Test for the 'dashboard' page
def test_dashboard():
    """
        Test case for the 'test_dashboard' method of the 'dashboard' class.
        """
    response = app.test_client().get('/dashboard')
    assert b"<h1>Welcome to the Dashboard</h1>" in response.data   # Assert that the response contains the specified header

# Test for the 'quiz' page
def test_quiz_page():
    """
        Test case for the 'test_quiz_page' method of the 'test_quiz_page' class.
        """
    response = app.test_client().get('/quiz')
    assert b"<h1>Quiz</h1>" in response.data   # Assert that the response contains the specified header
