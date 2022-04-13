import requests
from fastapi import status
from fastapi.testclient import TestClient

from src.api import app

client: requests.Session = TestClient(app)

anvdev_user = {"id": 28631927, "login": "anvdev", "name": "Ivan Titov"}


def test_user():
    response = client.put("/v1/users", json=anvdev_user)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get("/v1/users")
    assert response.json() == [anvdev_user]

    response = client.delete(f'/v1/users/{anvdev_user["id"]}')
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/v1/users")
    assert response.json() == []

    response = client.get(f'/v1/users/{anvdev_user["id"]}/stats')
    assert response.status_code == status.HTTP_200_OK
