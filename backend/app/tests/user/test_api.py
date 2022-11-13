def test_create_item(client):
    data = {
        "email": "user@example.com",
        "password": "string"
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == 201
