from tests.test_utils import generate_uuid, get_random_birthday
from tests.test_assertion_utils import assert_single_with_logging
from tests.api_tests.enums import ResponseStatus, ResponseCode


def test_delete_birthdays(api_client):
    random_birthday = get_random_birthday(api_client)

    api_client("DELETE", path_addon=random_birthday["uuid"])

    get_resonse_after_delete = api_client("GET")

    birthdays_after_delete = get_resonse_after_delete.json()["data"]
    assert_single_with_logging(
        "deleted birthday", random_birthday, "not in", birthdays_after_delete
    )

    get_single_response_after_delete = api_client("GET", path_addon=random_birthday["uuid"],
                                                  expected_response_format=ResponseStatus.ERROR,
                                                  expected_response_code=ResponseCode.NOT_FOUND)
    assert_single_with_logging(
        "Error message", get_single_response_after_delete.json()["message"], "==", "UUID not found"
    )


def test_delete_nonexistent_birthdays(api_client):
    delete_response = api_client("DELETE", path_addon=generate_uuid(),
                                 expected_response_format=ResponseStatus.ERROR,
                                 expected_response_code=ResponseCode.NOT_FOUND)
    assert_single_with_logging(
        "Error message", delete_response.json()["message"], "==", "UUID not found"
    )
