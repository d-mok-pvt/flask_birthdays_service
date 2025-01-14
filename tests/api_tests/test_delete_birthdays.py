from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.test_assertion_utils import  check_step
from tests.test_utils import generate_uuid, get_random_birthday


def test_delete_birthdays(api_client):
    random_birthday = get_random_birthday(api_client)

    api_client("DELETE", path_addon=random_birthday["uuid"])

    get_resonse_after_delete = api_client("GET")

    birthdays_after_delete = get_resonse_after_delete.json()["data"]

    check_step("birthday not in birthdays after delete",
               random_birthday not in birthdays_after_delete)

    get_single_response_after_delete = api_client("GET", path_addon=random_birthday["uuid"],
                                                  expected_response_format=ResponseStatus.ERROR,
                                                  expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to get birthday after delete",
               get_single_response_after_delete.json()["message"] == "UUID not found")


def test_delete_nonexistent_birthdays(api_client):
    delete_response = api_client("DELETE", path_addon=generate_uuid(),
                                 expected_response_format=ResponseStatus.ERROR,
                                 expected_response_code=ResponseCode.NOT_FOUND)

    check_step(
        "Error message", delete_response.json()["message"] == "UUID not found"
    )
