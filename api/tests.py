from django.test import TestCase
import requests

API_URL = "http://localhost:8000/"


def test_post_event():
    event_data = {
        "name": "Testcase entery",
        "attendants": [1],
        "starting_at": "2021-10-01T12:30:00+03:00",
        "password": "strongpassword",
    }
    response = requests.post(API_URL + "create-event/", data=event_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json().get("name", None) == "Testcase entery"
