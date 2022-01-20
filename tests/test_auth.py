def test_signup(client):
    """
    GIVEN a Flask application
    WHEN the '/signup' page is posted to (POST)
    THEN check the response is valid
    """
    response = client.post('/signup',
                            data=dict(name='Kalua', email='Kalua79@gmail.com', mobile='9638527417', password='KalUrl@1'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration request submitted" in response.data
    with client.session_transaction() as sess:
        assert sess['Registered'] == 'Y'

def test_login(client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = client.post('/login',
                                data=dict(email='yashgoyalcs@gmail.com', password='YasUrl@1'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"You are Successfully Logged In" in response.data
    with client.session_transaction() as sess:
        assert sess['cus_id'] == 'fe4b58bd1aaa44979d06d813c9601307'


def test_logout(client):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You are Successfully Logged Out" in response.data
    with client.session_transaction() as sess:
        assert 'cus_id' not in sess
        assert 'registered' not in sess