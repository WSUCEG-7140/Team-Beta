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

