from tests.test_utils import generate_name, generate_date, generate_uuid, get_random_birthday
from tests.test_assertion_utils import assert_single_with_logging, assert_multiple_with_logging
from tests.api_tests.enums import ResponseStatus, ResponseCode


def test_put_birthdays_only_name(api_client):
    random_birthday = get_random_birthday(api_client)

    new_name = generate_name()
    put_response = api_client(
        "PUT", path_addon=random_birthday["uuid"], json={"name": new_name})
    assert_single_with_logging(
        "New name returned in response", put_response.json()["data"]["name"], "==", new_name
    )

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    assert_multiple_with_logging(
        title="Returned resource parameters match PUT request parameters",
        conditions=(
            ("name", get_single_response.json()["data"]["name"], "==", new_name),
            ("date", get_single_response.json()["data"]["date"], "==", random_birthday["date"])
        )
    )


def test_put_birthdays_only_date(api_client):
    random_birthday = get_random_birthday(api_client)

    new_date = generate_date()
    put_response = api_client(
        "PUT", path_addon=random_birthday["uuid"], json={"date": new_date})
    assert_single_with_logging(
        "New date returned in response", put_response.json()["data"]["date"], "==", new_date
    )

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    assert_multiple_with_logging(
        title="Returned resource parameters match PUT request parameters",
        conditions=(
            ("name", get_single_response.json()["data"]["name"], "==", random_birthday["name"]),
            ("date", get_single_response.json()["data"]["date"], "==", new_date)
        )
    )


def test_put_birthdays_both_name_and_date(api_client):
    random_birthday = get_random_birthday(api_client)

    new_name = generate_name()
    new_date = generate_date()
    put_response = api_client("PUT", path_addon=random_birthday["uuid"], 
                              json={"name": new_name, "date": new_date})
    assert_multiple_with_logging(
        title="Response resource parameters match PUT request parameters",
        conditions=(
            ("name", put_response.json()["data"]["name"], "==", new_name),
            ("date", put_response.json()["data"]["date"], "==", new_date)
        )
    )

    get_single_response = api_client("GET", path_addon=random_birthday["uuid"])
    assert_multiple_with_logging(
        title="Returned resource parameters match PUT request parameters",
        conditions=(
            ("name", get_single_response.json()["data"]["name"], "==", new_name),
            ("date", get_single_response.json()["data"]["date"], "==", new_date)
        )
    )


def test_put_nonexistent_birthdays(api_client):
    put_response = api_client("PUT", path_addon=generate_uuid(),
                              json={"name": generate_name(), "date": generate_date()},
                              expected_response_format=ResponseStatus.ERROR, 
                              expected_response_code=ResponseCode.NOT_FOUND)
    assert_single_with_logging(
        "Error message", put_response.json()["message"], "==", "UUID not found"
    )


def test_put_birthdays_no_json(api_client):
    random_birthday = get_random_birthday(api_client)

    put_response = api_client("PUT", path_addon=random_birthday["uuid"], json={},
                              expected_response_format=ResponseStatus.ERROR, 
                              expected_response_code=ResponseCode.BAD_REQUEST)
    assert_single_with_logging(
        "Error definition", put_response.json()["data"], "==", "At least one of 'name' or 'date' is required."
    )

