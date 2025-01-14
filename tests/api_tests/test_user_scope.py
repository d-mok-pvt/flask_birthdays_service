from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.conftest import setup_user_2
from tests.test_assertion_utils import check_step
from tests.test_utils import get_random_birthday


def test_get_other_user_birthdays(api_client, setup_user_2):
    random_birthday = get_random_birthday(api_client)
    get_single_response_after_delete = api_client("GET",
                                                  auth=(setup_user_2.username, setup_user_2.password),
                                                  path_addon=random_birthday["uuid"],
                                                  expected_response_format=ResponseStatus.ERROR,
                                                  expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to get other user's birthday",
               get_single_response_after_delete.json()["message"] == "UUID not found")