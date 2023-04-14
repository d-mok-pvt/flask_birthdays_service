import allure
import pytest


def get_result(value_1, operator, value_2):
    valid_operators = ["==", "!=", ">", ">=", "<", "<=", "in", "not in", "is not"]
    try:
        if operator in valid_operators:
            if operator == "==":
                return value_1 == value_2
            elif operator == "!=":
                return value_1 != value_2
            elif operator == ">":
                return value_1 > value_2
            elif operator == ">=":
                return value_1 >= value_2
            elif operator == "<":
                return value_1 < value_2
            elif operator == "<=":
                return value_1 <= value_2
            elif operator == "in":
                return value_1 in value_2
            elif operator == "not in":
                return value_1 not in value_2
            elif operator == "is not":
                return value_1 is not value_2
        else:
            raise ValueError(f"Invalid operator: {operator}")
    except ValueError as e:
        # Handle the exception as appropriate for your use case
        print(f"Error: {e}")


def assert_single_with_logging(assert_title: str, value_1, operator: str, value_2):
    with allure.step(f"Assert: {assert_title} {operator} {str(value_2)[:100]}"):
        result = get_result(value_1, operator, value_2)
        if result:
            pass
        else:
            pytest.fail(f"Assertion failed: {assert_title} {operator} {value_2}")


@allure.step("Assert All: {title}")
def assert_multiple_with_logging(title: str, conditions):
    for i, condition in enumerate(conditions):
        assert_title, value_1, operator, value_2 = condition
        result = get_result(value_1, operator, value_2)
        message = f"{i+1}. {assert_title} {operator} {str(value_2)[:100]}"
        if result:
            with allure.step(message):
                pass
        else:
            with allure.step(message):
                pytest.fail(f"Assertion failed: {assert_title} {operator} {value_2}")


