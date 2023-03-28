import random
from tests.test_utils import generate_uuid


def test_delete_birthdays(api_client, check_successful_response):
    get_response = api_client("GET")
    check_successful_response(get_response)
    birthdays = get_response.json()["data"]
    random_birthday = random.choice(birthdays)

    delete_response = api_client("DELETE", endpoint=random_birthday["uuid"])
    check_successful_response(delete_response)

    get_resonse_after_delete = api_client("GET")
    check_successful_response(get_resonse_after_delete)
    birthdays_after_delete = get_resonse_after_delete.json()["data"]
    assert random_birthday not in birthdays_after_delete


def test_delete_nonexistent_birthdays(api_client, check_error_response):
    delete_response = api_client("DELETE", endpoint=generate_uuid())
    check_error_response(delete_response, 404)
    assert delete_response.json()["message"] == "UUID not found"
