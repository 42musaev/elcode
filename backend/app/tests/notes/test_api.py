def test_login_user(client, user_token):
    response = client.get("/api/v1/notes/health-check", headers={
        "authorization": f"Bearer {user_token['access_token']}"
    })
    assert response.status_code == 200


def test_create_note(client):
    data_user = {
        "title": "example",
        "body": "import os"
    }
    response = client.post("/api/v1/notes", json=data_user)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json['title'] == data_user['title']
    assert response_json['body'] == data_user['body']
