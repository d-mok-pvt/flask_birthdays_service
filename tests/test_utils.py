from faker import Faker
import random


def generate_name() -> str:
    """Generate a random person name using the Faker library."""
    fake = Faker()
    return fake.name()


def generate_date() -> str:
    """Generate a random date using the Faker library."""
    fake = Faker()
    return fake.date()


def generate_uuid() -> str:
    """Generate a random UUID using the Faker library."""
    fake = Faker()
    return fake.uuid4()


def get_random_birthday(api_client):
    get_response = api_client("GET")
    birthdays = get_response.json()["data"]
    return random.choice(birthdays)
