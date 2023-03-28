import random
from tests.test_utils import generate_name, generate_date, generate_uuid


def test_put_birthdays_only_name(api_client, check_successful_response):
    get_response = api_client("GET")
    check_successful_response(get_response)
    birthdays = get_response.json()["data"]
    random_birthday = random.choice(birthdays)

    new_name = generate_name()
    put_response = api_client(
        "PUT", endpoint=random_birthday["uuid"], json={"name": new_name})
    check_successful_response(put_response)
    assert put_response.json()["data"]["name"] == new_name

    get_single_response = api_client("GET", endpoint=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json()["data"][0]["name"] == new_name
    assert get_single_response.json(
    )["data"][0]["date"] == random_birthday["date"]


def test_put_birthdays_only_date(api_client, check_successful_response):
    get_response = api_client("GET")
    check_successful_response(get_response)
    birthdays = get_response.json()["data"]
    random_birthday = random.choice(birthdays)

    new_date = generate_date()
    put_response = api_client(
        "PUT", endpoint=random_birthday["uuid"], json={"date": new_date})
    check_successful_response(put_response)
    assert put_response.json()["data"]["date"] == new_date

    get_single_response = api_client("GET", endpoint=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json(
    )["data"][0]["name"] == random_birthday["name"]
    assert get_single_response.json()["data"][0]["date"] == new_date


def test_put_birthdays_both_name_and_date(api_client, check_successful_response):
    get_response = api_client("GET")
    check_successful_response(get_response)
    birthdays = get_response.json()["data"]
    random_birthday = random.choice(birthdays)

    new_name = generate_name()
    new_date = generate_date()
    put_response = api_client("PUT", endpoint=random_birthday["uuid"], json={
                              "name": new_name, "date": new_date})
    check_successful_response(put_response)
    assert put_response.json()["data"]["name"] == new_name
    assert put_response.json()["data"]["date"] == new_date

    get_single_response = api_client("GET", endpoint=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json()["data"][0]["name"] == new_name
    assert get_single_response.json()["data"][0]["date"] == new_date


def test_put_nonexistent_birthdays(api_client, check_error_response):
    put_response = api_client("PUT", endpoint=generate_uuid(),
                              json={"name": generate_name(), "date": generate_date()})
    check_error_response(put_response, 404)
    assert put_response.json()["message"] == "UUID not found"
