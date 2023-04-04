from tests.test_utils import generate_name, generate_date, generate_uuid, get_random_birthday


def test_put_birthdays_only_name(api_client, check_successful_response):
    random_birthday = get_random_birthday(api_client, check_successful_response)

    new_name = generate_name()
    put_response = api_client(
        "PUT", path_addon=random_birthday["uuid"], json={"name": new_name})
    check_successful_response(put_response)
    assert put_response.json()["data"]["name"] == new_name

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json()["data"]["name"] == new_name
    assert get_single_response.json(
    )["data"]["date"] == random_birthday["date"]


def test_put_birthdays_only_date(api_client, check_successful_response):
    random_birthday = get_random_birthday(api_client, check_successful_response)

    new_date = generate_date()
    put_response = api_client(
        "PUT", path_addon=random_birthday["uuid"], json={"date": new_date})
    check_successful_response(put_response)
    assert put_response.json()["data"]["date"] == new_date

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json(
    )["data"]["name"] == random_birthday["name"]
    assert get_single_response.json()["data"]["date"] == new_date


def test_put_birthdays_both_name_and_date(api_client, check_successful_response):
    random_birthday = get_random_birthday(api_client, check_successful_response)

    new_name = generate_name()
    new_date = generate_date()
    put_response = api_client("PUT", path_addon=random_birthday["uuid"], json={
                              "name": new_name, "date": new_date})
    check_successful_response(put_response)
    assert put_response.json()["data"]["name"] == new_name
    assert put_response.json()["data"]["date"] == new_date

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    check_successful_response(get_single_response)
    assert get_single_response.json()["data"]["name"] == new_name
    assert get_single_response.json()["data"]["date"] == new_date


def test_put_nonexistent_birthdays(api_client, check_error_response):
    put_response = api_client("PUT", path_addon=generate_uuid(),
                              json={"name": generate_name(), "date": generate_date()})
    check_error_response(put_response, 404)
    assert put_response.json()["message"] == "UUID not found"


def test_put_birthdays_no_json(api_client,check_successful_response, check_error_response):
    random_birthday = get_random_birthday(api_client, check_successful_response)

    put_response = api_client("PUT", path_addon=random_birthday["uuid"], json={})
    check_error_response(put_response, 400)
    assert put_response.json(
    )["data"] == "At least one of 'name' or 'date' is required."
