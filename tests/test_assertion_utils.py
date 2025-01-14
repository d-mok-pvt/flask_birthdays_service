import allure
import pytest


def check_step(title: str, condition: bool):
    with allure.step("🔍 " + title):
        if not condition:
            pytest.fail(f"Assertion failed: {title}")

def check_list(title: str, conditions: list[tuple[str, bool]]):
    with allure.step("🔍 " + title):
        for condition in conditions:
            check_step(*condition)

def check_successful_response(response, status_code=200):
    check_list("Check successful response", [
        (f"Status code is {status_code}", response.status_code == status_code),
        ("Length > 0", len(response.json()) > 0),
        ("Status is success", response.json()["status"] == "success")
    ])


def check_error_response(response, status_code):
    check_list("Check error response", [
        (f"Status code is {status_code}", response.status_code == status_code),
        ("Length > 0", len(response.json()) > 0),
        ("Status is error", response.json()["status"] == "error")
    ])



