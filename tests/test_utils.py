import logging
import random

import allure
import requests
from faker import Faker

from tests.classes.user import User
from tests.test_config import USERS_API_URL

fake = Faker()


def generate_name() -> str:
    return fake.name()

def generate_password() -> str:
    return fake.password(length=12)

def generate_date() -> str:
    return fake.date()


def generate_uuid() -> str:
    return fake.uuid4()

def create_user() -> User:
    username = generate_name()
    password = generate_password()
    userid = create_user_request(username, password).json()["data"]["userid"]
    return User(username = username, password = password, userid = userid)


@allure.step("Get random birthday")
def get_random_birthday(api_client):
    get_response = api_client("GET")
    birthdays = get_response.json()["data"]
    return random.choice(birthdays)


def create_user_request(username, password):
    url = f"{USERS_API_URL}/user"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Created user {payload}")
    logging.info(response.json())
    return response
