from tests.test_utils import generate_name, generate_date


def test_post_birthdays(api_client, check_successful_response):
    data = {
        "name": generate_name(),
        "date": generate_date()
    }
    post_response = api_client("POST", json=data)
    assert post_response.status_code == 201
    check_successful_response(post_response)
    assert post_response.json()["data"]["name"] == data["name"]
    assert post_response.json()["data"]["date"] == data["date"]
    assert post_response.json()["data"]["uuid"] is not None

    get_single_response = api_client(
        "GET", endpoint=post_response.json()["data"]["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json()["data"][0]["name"] == data["name"]
    assert get_single_response.json()["data"][0]["date"] == data["date"]
