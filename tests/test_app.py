from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to our Dad Jokes Application. 👨"}


def test_get_joke():
    response = client.get("/joke")
    assert response.status_code == 200


def test_create_joke():
    response = client.post("/joke", json={"joke": "foobar"})
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_get_joke_by_id():
    response = client.get("/joke/1")
    assert response.status_code == 200
    assert response.json() == {"joke": "I'm afraid for the calendar. Its days are numbered."}



def test_update_joke():
    response = client.put("/joke/2", json={"joke": "test"})
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_get_jokes():
    response = client.get("/jokes")
    assert response.status_code == 200


def test_get_jokes_with_limit():
    response = client.get("/jokes?limit=2")
    assert response.status_code == 200


def test_get_jokes_post():
    response = client.post("/jokes?limit=2")
    assert response.status_code == 405