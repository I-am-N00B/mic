import requests

base_url = 'http://localhost:8000'
add_painting_url = f'{base_url}/add_painting'
get_paintings_url = f'{base_url}/get_paintings'
get_painting_by_id_url = f'{base_url}/get_painting_by_id'
update_painting_url = f'{base_url}/update_painting'
delete_painting_url = f'{base_url}/delete_painting'

new_painting = {
    "id" : 99,
    "title": "Starry Night",
    "artist": "Vincent van Gogh",
    "year": 1889,
    "description": "A depiction of the view from the east-facing window of his asylum room at Saint-Rémy-de-Provence."
}


def test_add_painting():
    res = requests.post(add_painting_url, json=new_painting)
    assert res.status_code == 200


def test_get_paintings():
    res = requests.get(get_paintings_url).json()
    assert any(p['title'] == "Starry Night" for p in res)


def test_get_painting_by_id():
    res = requests.get(f"{get_painting_by_id_url}?painting_id=99").json()
    assert res['title'] == "Starry Night"


def test_update_painting():
    updated_painting = {
        "id" : 99,
        "title": "Starry Night",
        "artist": "Vincent van Gogh",
        "year": 1889,
        "description": "Updated description of the Starry Night"
    }
    res = requests.put(f"{update_painting_url}?painting_id=99", json=updated_painting)
    updated_data = res.json()
    assert res.status_code == 200
    assert updated_data['description'] == "Updated description of the Starry Night"


def test_delete_painting():
    res = requests.delete(f"{delete_painting_url}?painting_id=99").json()
    assert res == {"message": "Painting deleted"}
