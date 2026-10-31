def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_read_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Cloud Guestbook" in response.text


def test_sign_and_list_flow(client):
    # Submit a new signature via form data
    response = client.post("/sign", data={"name": "Isolated Tester"}, follow_redirects=True)
    assert response.status_code == 200

    # Verify the signature appears on the list page
    response = client.get("/list")
    assert response.status_code == 200
    assert "Isolated Tester" in response.text