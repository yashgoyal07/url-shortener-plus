def test_slink_it(client):
    """
    GIVEN a Flask application
    WHEN the '/slink_it' page is posted to (POST)
    THEN check the response is valid
    """
    response = client.post('/slink_it',
                        data=dict(long_link='https://www.google.com/search?q=71%2B26&ei=ilLoYc7mHNmE4t4PrvuMiAg&ved=0ahUKEwjO0-Wrs771AhVZgtgFHa49A4EQ4dUDCA4&uact=5&oq=71%2B26&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgUILhCRAjoFCAAQkQI6CwgAEIAEELEDEIMBOggILhCABBCxAzoICC4QsQMQkQI6CwgAELEDEIMBEJECOggIABCABBCxAzoECAAQQ0oECEEYAEoECEYYAFAAWJQVYIoXaAFwAHgBgAG7AogBjBCSAQUyLTcuMZgBAKABAbABAMABAQ&sclient=gws-wiz'),
                        follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Slink Creation Request Submit" in response.data

def test_root(client):
    """
    GIVEN a Flask application
    WHEN the '/slink_it' page is posted to (POST)
    THEN check the response is valid
    """

    response = client.get('/', follow_redirects=True)

    assert response.status_code == 200
    assert b"Shorten Your Link Using Slink!" in response.data
    assert b"SLINK" in response.data

