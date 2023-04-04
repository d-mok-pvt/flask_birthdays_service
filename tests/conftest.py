import pytest
import requests
from tests.test_config import API_URL
import logging
from tests.test_data_preparation import prepare_database
import allure
import json
import requests_to_curl

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
    def _send_request(method, base_url=API_URL, path_addon=None, **kwargs):
        url = base_url if path_addon is None else f"{base_url}/{path_addon}"

        response = requests.request(method, url, headers=headers, **kwargs)
        curl_command = requests_to_curl.parse(response, return_it=True)
        allure.attach(curl_command, "cURL",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(dict(response.headers), indent=4),
                      "Response headers", attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(response.json(), indent=4),
                      "Response body", attachment_type=allure.attachment_type.JSON)

        return response

    yield _send_request


@pytest.fixture
def check_successful_response():
    def _check_successful_response(response):
        assert response.status_code == 200 or response.status_code == 201
        assert len(response.json()) > 0
        assert response.json()["status"] == "success"
    return _check_successful_response


@pytest.fixture
def check_error_response():
    def _check_error_response(response, status_code):
        assert response.status_code == status_code
        assert len(response.json()) > 0
        assert response.json()["status"] == "error"
    return _check_error_response
