

def test_hello_world(client):

    response = client.get("/")

    assert response.data.decode('utf-8') == 'Hello, World!'
