from tests.test_utils import generate_uuid, get_random_birthday


def test_delete_birthdays(api_client, check_successful_response, check_error_response):
    random_birthday = get_random_birthday(api_client, check_successful_response)

    delete_response = api_client("DELETE", path_addon=random_birthday["uuid"])
    check_successful_response(delete_response)

    get_resonse_after_delete = api_client("GET")
    check_successful_response(get_resonse_after_delete)
    birthdays_after_delete = get_resonse_after_delete.json()["data"]
    assert random_birthday not in birthdays_after_delete

    get_single_response_after_delete = api_client(
        "GET", path_addon=random_birthday["uuid"])
    check_error_response(get_single_response_after_delete, 404)


def test_delete_nonexistent_birthdays(api_client, check_error_response):
    delete_response = api_client("DELETE", path_addon=generate_uuid())
    check_error_response(delete_response, 404)
    assert delete_response.json()["message"] == "UUID not found"
