def test_create_user(client):
    data_user = {
        "email": "user@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/users", json=data_user)
    response_json = response.json()
    response_json.pop('id')
    assert response.status_code == 201
    assert response_json['email'] == data_user['email']


def test_login_user(client, user_token):
    response = client.get(
        "/api/v1/health-check",
        headers={"authorization": f"Bearer {user_token['access_token']}"}
    )
    assert response.status_code == 200
    response = client.post(
        "/api/v1/token-refresh",
        params={"refresh_token": user_token['refresh_token']}
    )
    assert response.status_code == 200
