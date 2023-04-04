from tests.test_utils import generate_name, generate_date
from tests.test_assertion_utils import assert_single_with_logging, assert_multiple_with_logging


def test_post_birthdays(api_client, check_successful_response):
    data = {
        "name": generate_name(),
        "date": generate_date()
    }
    post_response = api_client("POST", json=data)
    assert_single_with_logging("Response code", post_response.status_code, "==", 201)
    check_successful_response(post_response)
    assert_multiple_with_logging(
        title="Response resource parameters are consistent with the request creation of parameters",
        conditions=(
            ("name", post_response.json()["data"]["name"], "==", data["name"]),
            ("date", post_response.json()["data"]["date"], "==", data["date"]),
            ("uuid", post_response.json()["data"]["uuid"], "is not", None)
        )
    )

    get_single_response = api_client(
        "GET", path_addon=post_response.json()["data"]["uuid"])
    check_successful_response(get_single_response)
    assert_multiple_with_logging(
        title="Returned resource parameters are consistent with the request creation of parameters",
        conditions=(
            ("name", get_single_response.json()["data"]["name"], "==", data["name"]),
            ("date", get_single_response.json()["data"]["date"], "==", data["date"])
        )
    )

    api_client("DELETE", path_addon=post_response.json()["data"]["uuid"])


def test_post_birthdays_without_name(api_client, check_error_response):
    data = {
        "date": generate_date()
    }
    post_response = api_client("POST", json=data)
    check_error_response(post_response, 400)
    assert_multiple_with_logging(title= "Response error is valid", conditions= (
        ("error message", post_response.json()["message"], "==", "Invalid request parameters"),
        ("error definition", post_response.json()["data"]["name"][0], "==", "This field is required.")
    ))


def test_post_birthdays_without_date(api_client, check_error_response):
    data = {
        "name": generate_name()
    }
    post_response = api_client("POST", json=data)
    check_error_response(post_response, 400)
    assert_multiple_with_logging(title="Returned error is valid", conditions=(
        ("error message", post_response.json()["message"], "==", "Invalid request parameters"),
        ("error definition", post_response.json()["data"]["date"][0], "==", "This field is required.")
    ))

