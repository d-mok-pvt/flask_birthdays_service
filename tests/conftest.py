import json
import logging

import allure
import pytest
import requests
import requests_to_curl

from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.test_assertion_utils import check_list, check_successful_response, check_error_response
from tests.test_config import BIRTHDAYS_API_URL
from tests.test_data_preparation import prepare_database
from tests.test_utils import create_user

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session", autouse=True)
def setup_user_1():
    return create_user()


@pytest.fixture(scope="session", autouse=True)
def setup_user_2():
    return create_user()

@pytest.fixture()
def api_client(setup_user_1):
    headers = {"Content-Type": "application/json"}

    @allure.step("{method} request to {base_url}")
    def _send_request(method, base_url=BIRTHDAYS_API_URL, path_addon=None,
                      auth=(setup_user_1.username, setup_user_1.password),
                      expected_response_format: ResponseStatus = ResponseStatus.SUCCESS,
                      expected_response_code: ResponseCode = ResponseCode.SUCCESS, **kwargs):
        url = base_url if path_addon is None else f"{base_url}/{path_addon}"

        response = requests.request(method, url, headers=headers, auth=auth, **kwargs)
        curl_command = requests_to_curl.parse(response, return_it=True)
        allure.attach(curl_command, "cURL",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps({
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json()
        }, indent=4), "Response data", attachment_type=allure.attachment_type.JSON)

        if expected_response_format == ResponseStatus.SUCCESS:
            check_successful_response(response, expected_response_code.value)
        elif expected_response_format == ResponseStatus.ERROR:
            check_error_response(response, expected_response_code.value)

        return response

    yield _send_request

