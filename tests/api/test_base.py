from fastapi import testclient


def test_base(client: testclient.TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Time Tracker!"}
