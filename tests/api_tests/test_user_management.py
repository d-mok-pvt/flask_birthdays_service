from tests.api_tests.enums import ResponseStatus, ResponseCode
from tests.classes.user import User
from tests.test_config import USERS_API_URL
from tests.test_utils import generate_name, generate_uuid, create_user, generate_password


def test_post_user(api_client):
    new_user = {
        "username": generate_name(),
        "password": generate_password()
    }
    api_client("POST", base_url=USERS_API_URL, path_addon="/user", json=new_user,
                               expected_response_format=ResponseStatus.SUCCESS,
                               expected_response_code=ResponseCode.CREATED)
    api_client("GET", auth=(new_user["username"], new_user["password"]),
               expected_response_format=ResponseStatus.SUCCESS,
               expected_response_code=ResponseCode.SUCCESS)


def test_post_user_validation_error(api_client):
    invalid_user = {
        "username": generate_name()
    }
    api_client("POST", base_url=USERS_API_URL, path_addon="/user", json=invalid_user,
               expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.BAD_REQUEST)


def test_delete_user(api_client):
    new_user: User = create_user()
    api_client("DELETE", base_url=USERS_API_URL, path_addon=f"/{new_user.userid}")
    api_client("GET", auth=(new_user.username, new_user.password),
               expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.UNAUTHORIZED)


def test_delete_user_not_found(api_client):
    user_id = generate_uuid()
    api_client("DELETE", base_url=USERS_API_URL, path_addon=f"/{user_id}",
               expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.NOT_FOUND)


def test_put_user_password(api_client):
    new_user: User = create_user()
    new_password = {
        "new_password": generate_password()
    }
    api_client("PUT", base_url=USERS_API_URL, path_addon=f"/{new_user.userid}/password", json=new_password)
    api_client("GET", auth=(new_user.username, new_user.password),
               expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.UNAUTHORIZED)
    api_client("GET", auth=(new_user.username, new_password["new_password"]),
               expected_response_format=ResponseStatus.SUCCESS,
               expected_response_code=ResponseCode.SUCCESS)


def test_put_user_password_validation_error(api_client):
    user_id = generate_uuid()
    empty_password = {}
    api_client("PUT", base_url=USERS_API_URL, path_addon=f"/{user_id}/password",
               json=empty_password, expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.BAD_REQUEST)


def test_put_user_password_not_found(api_client):
    user_id = generate_uuid()
    new_password = {
        "new_password": generate_password()
    }
    api_client("PUT", base_url=USERS_API_URL, path_addon=f"/{user_id}/password", json=new_password,
               expected_response_format=ResponseStatus.ERROR,
               expected_response_code=ResponseCode.NOT_FOUND)
