import pytest
import requests
from tests.test_config import API_URL
import logging
from tests.test_data_preparation import prepare_database
import allure
import json
import requests_to_curl
from tests.test_assertion_utils import assert_multiple_with_logging
from tests.api_tests.enums import ResponseStatus, ResponseCode


logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session", autouse=True)
def setup_database(prepare_database):
    # This fixture will automatically run the `prepare_database` fixture
    # creates test data before any tests are run. And clear test data after all tests are finished.
    pass


@pytest.fixture()
def api_client():
    headers = {"Content-Type": "application/json"}

    @allure.step("{method} request to {base_url}")
    def _send_request(method, base_url=API_URL, path_addon=None, 
                      expected_response_format : ResponseStatus = ResponseStatus.SUCCESS, 
                      expected_response_code: ResponseCode = ResponseCode.SUCCESS, **kwargs):
        url = base_url if path_addon is None else f"{base_url}/{path_addon}"

        response = requests.request(method, url, headers=headers, **kwargs)
        curl_command = requests_to_curl.parse(response, return_it=True)
        allure.attach(curl_command, "cURL",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(dict(response.headers), indent=4),
                      "Response headers", attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(response.json(), indent=4),
                      "Response body", attachment_type=allure.attachment_type.JSON)
        
        if expected_response_format == ResponseStatus.SUCCESS:
            check_successful_response(response, expected_response_code.value)
        elif expected_response_format == ResponseStatus.ERROR:
            check_error_response(response, expected_response_code.value)

        return response

    yield _send_request


def check_successful_response(response, status_code = 200):
    assert_multiple_with_logging(title= "Assertion default successful response format is valid", conditions= (
        ("Response status code", response.status_code, "==", status_code),
        ("Response lenght", len(response.json()), ">", 0),
        ("Response status", response.json()["status"], "==", "success")
    ))


def check_error_response(response, status_code):
    assert_multiple_with_logging(title= "Assertion default error response format is valid", conditions= (
        ("Response status code", response.status_code, "==", status_code),
        ("Response lenght", len(response.json()), ">", 0),
        ("Response status", response.json()["status"], "==", "error")
    ))
