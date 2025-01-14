from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.test_assertion_utils import check_list
from tests.test_utils import generate_name, generate_date


def test_post_birthdays(api_client):
    data = {
        "name": generate_name(),
        "date": generate_date()
    }
    post_response = api_client("POST", json=data, expected_response_code=ResponseCode.CREATED)
    check_list("Response resource parameters match creation request parameters", [
        ("name", post_response.json()["data"]["name"] == data["name"]),
        ("date", post_response.json()["data"]["date"] == data["date"]),
        ("uuid is not None", post_response.json()["data"]["uuid"] is not None)
    ]
               )

    get_single_response = api_client(
        "GET", path_addon=post_response.json()["data"]["uuid"])
    check_list("Response resource parameters match creation request parameters", [
        ("name", get_single_response.json()["data"]["name"] == data["name"]),
        ("date", get_single_response.json()["data"]["date"] == data["date"])
    ]
               )

    api_client("DELETE", path_addon=post_response.json()["data"]["uuid"])


def test_post_birthdays_without_name(api_client):
    data = {
        "date": generate_date()
    }
    post_response = api_client("POST", json=data,
                               expected_response_format=ResponseStatus.ERROR,
                               expected_response_code=ResponseCode.BAD_REQUEST)
    check_list("Returned error is valid", [
        ("error message", post_response.json()["message"] == "Invalid request parameters"),
        ("error definition", post_response.json()["data"]["name"][0] == "This field is required.")
    ])


def test_post_birthdays_without_date(api_client):
    data = {
        "name": generate_name()
    }
    post_response = api_client("POST", json=data,
                               expected_response_format=ResponseStatus.ERROR,
                               expected_response_code=ResponseCode.BAD_REQUEST)
    check_list("Returned error is valid", [
        ("error message", post_response.json()["message"] == "Invalid request parameters"),
        ("error definition", post_response.json()["data"]["date"][0] == "This field is required.")
    ])
