from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.conftest import setup_user_2
from tests.test_assertion_utils import check_step
from tests.test_utils import get_random_birthday, generate_name, generate_date


def test_get_other_user_birthdays(api_client, setup_user_2):
    random_birthday = get_random_birthday(api_client)
    get_single_response_after_delete = api_client("GET",
                                                  auth=(setup_user_2.username, setup_user_2.password),
                                                  path_addon=random_birthday["uuid"],
                                                  expected_response_format=ResponseStatus.ERROR,
                                                  expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to get other user's birthday",
               get_single_response_after_delete.json()["message"] == "UUID not found")


def test_modify_other_user_birthday(api_client, setup_user_2):
    data = {
        "name": generate_name(),
        "date": generate_date()
    }
    post_response = api_client("POST",
                               auth=(setup_user_2.username, setup_user_2.password),
                               json=data, expected_response_code=ResponseCode.CREATED)
    bdayid = post_response.json()["data"]["uuid"]

    get_single_response = api_client("GET", path_addon=bdayid,
                                     expected_response_format=ResponseStatus.ERROR,
                                     expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to get other user's resource",
               get_single_response.json()["message"] == "UUID not found")

    put_response = api_client("PUT", path_addon=bdayid,
                              json={"name": generate_name(), "date": generate_date()},
                              expected_response_format=ResponseStatus.ERROR,
                              expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to modify other user's resource",
               put_response.json()["message"] == "UUID not found")

    delete_response = api_client("DELETE", path_addon=bdayid,
                                 expected_response_format=ResponseStatus.ERROR,
                                 expected_response_code=ResponseCode.NOT_FOUND)
    check_step("Got error trying to delete other user's resource",
               delete_response.json()["message"] == "UUID not found")
