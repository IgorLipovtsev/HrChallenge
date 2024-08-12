from playwright.sync_api import Playwright, sync_playwright
from datetime import datetime
import numpy as np
import pytest


@pytest.mark.parametrize("user_id", [10, 15, 33, 94, 501, 911])
def test_response_get_male_users(playwright: Playwright, user_id) -> None:
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/user/{user_id}")
    data = response.json()

    try:
        assert response.status == 200, f"Expected status 200 , actually got {response.status}"
        assert response.status_text == "OK", f"Expected status text 'OK', actually got '{response.status_text}'"
        assert data['errorCode'] == 0, f"Expected errorCode 0, actually got {data['errorCode']}"
        assert data['user']['id'] == user_id, f"Expected user ID {user_id} , actually got {data['user']['id']}"
        assert data['user']['gender'] == 'male', f"Expected gender 'male' , actually got '{data['user']['gender']}'"
        assert isinstance(data['isSuccess'], bool), "Value is not a boolean"
        assert response.headers['content-type'] == 'application/json;charset=UTF-8'

        # Проверяем, что значения Age и Id находятся в пределах Int32
        np.int32(data['errorCode'])
        np.int32(data['user']['id'])

        # Проверяем валидность значения registrationDate
        datetime.fromisoformat(data['user']['registrationDate'])

    except ValueError as ve:
        raise AssertionError(f"Invalid ISO datetime format for user ID {user_id}: {ve}")
    except OverflowError as oe:
        raise AssertionError(f"Int value out of bounds for int32 for user ID {user_id}: {oe}")

@pytest.mark.parametrize("user_id", [5, 15, 16, 300, 502, 503])
def test_response_get_female_users(playwright: Playwright, user_id) -> None:
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/user/{user_id}")
    data = response.json()

    try:
        assert response.status == 200, f"Expected status 200, actually got {response.status}"
        assert response.status_text == "OK", f"Expected status text 'OK', actually got '{response.status_text}'"
        assert data['errorCode'] == 0, f"Expected errorCode 0, actually got {data['errorCode']}"
        assert data['user']['id'] == user_id, f"Expected user ID {user_id} , actually got {data['user']['id']}"
        assert data['user']['gender'] == 'female', f"Expected gender 'female', actually got '{data['user']['gender']}'"
        assert isinstance(data['isSuccess'], bool), "Value is not a boolean"
        assert response.headers['content-type'] == 'application/json;charset=UTF-8'

        # Проверяем, что значения Age и Id находятся в пределах Int32
        np.int32(data['errorCode'])
        np.int32(data['user']['id'])

        # Проверяем валидность значения registrationDate
        datetime.fromisoformat(data['user']['registrationDate'])

    except ValueError as ve:
        raise AssertionError(f"Invalid ISO datetime format for user ID {user_id}: {ve}")
    except OverflowError as oe:
        raise AssertionError(f"Int value out of bounds for int32 for user ID {user_id}: {oe}")


def test_response_with_no_id(playwright: Playwright) -> None:
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/user/")

    assert response.status == 404, f"Expected status 200, actually got {response.status}"
    assert response.status_text == "Not Found", f"Expected status text 'Not Found', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'


def test_response_with_non_existed_user(playwright: Playwright) -> None:
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/user/55")
    data = response.json()
    assert response.status == 200, f"Expected status 200, actually got {response.status}"
    assert response.status_text == "OK", f"Expected status text 'OK', actually got '{response.status_text}'"
    assert data['user'] is None, f"User already existed and found"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'


def test_response_post_method(playwright: Playwright) -> None:
    context = playwright.request.new_context()
    response = context.post(url=f"https://hr-challenge.dev.tapyou.com/api/test/user/55")
    data = response.json()

    assert data['message'] == "Request method 'POST' not supported"
    assert response.status == 405, f"Expected status code 405, actually got {response.status}"
    assert response.status_text == "Method Not Allowed", f"Expected status text 'Internal Server Error', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'
