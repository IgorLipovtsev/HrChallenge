import pytest
from playwright.sync_api import Playwright, sync_playwright

@pytest.fixture()
def get_male_users(playwright: Playwright) -> list:
    # browser = playwright.chromium.launch(headless=False)
    context = playwright.request.new_context()
    response = context.get(url="https://hr-challenge.dev.tapyou.com/api/test/users?gender=male")
    data = response.json()

    assert response.status == 200, f"Expected status 200, actually got {response.status}"
    assert response.status_text == "OK", f"Expected status text 'OK', actually got '{response.status_text}'"
    assert data['errorCode'] == 0
    assert response.ok
    assert isinstance(data['isSuccess'], bool), "Value is not a boolean"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'


    return data['idList']

@pytest.fixture()
def get_female_users(playwright: Playwright) -> list:
    # browser = playwright.chromium.launch(headless=False)
    context = playwright.request.new_context()
    response = context.get(url="https://hr-challenge.dev.tapyou.com/api/test/users?gender=female")
    data = response.json()

    assert response.status == 200, f"Expected status 200, actually  {response.status}"
    assert response.status_text == "OK", f"Expected status text 'OK', actually got '{response.status_text}'"
    assert data['errorCode'] == 0
    assert response.ok
    assert isinstance(data['isSuccess'], bool), "Value is not a boolean"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'


    return data['idList']

def test_get_fake_gender_users(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False)
    context = playwright.request.new_context()
    response = context.get(url="https://hr-challenge.dev.tapyou.com/api/test/users?gender=noone")
    data = response.json()

    assert data['error'] == "Internal Server Error"
    assert response.status == 500, f"Expected status code 500, actually got {response.status}"
    assert response.status_text == "Internal Server Error", f"Expected status text 'Internal Server Error', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'

def test_get_mccloud_users(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False)
    context = playwright.request.new_context()
    response = context.get(url="https://hr-challenge.dev.tapyou.com/api/test/users?gender=McCloud")
    data = response.json()

    assert data['error'] == "Internal Server Error"
    assert response.status == 500, f"Expected status code 500, actually got {response.status}"
    assert response.status_text == "Internal Server Error", f"Expected status text 'Internal Server Error', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'

def test_find_duplicate_users(get_male_users, get_female_users):
    duplicate_user_id = []
    for element in get_male_users:
        if element in get_female_users and element not in duplicate_user_id:
            duplicate_user_id.append(element)

    assert duplicate_user_id == True, f"User Id {duplicate_user_id} found in both gender lists, please investigate!"

def test_response_missing_gender_param(playwright: Playwright) -> None:
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/users")
    data = response.json()
    print(data)
    assert data['message'] == "Required String parameter 'gender' is not present"
    assert response.status == 400, f"Expected status code 400, actually got {response.status}"
    assert response.status_text == "Bad Request", f"Expected status text 'Bad Request', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'

@pytest.mark.parametrize("user_gender", ['Male', "Female", "FEMALE", "MALE", 'mccloud', 'MAGIC'])
def test_get_uppercase_users(playwright: Playwright, user_gender) -> None:
    # browser = playwright.chromium.launch(headless=False)
    context = playwright.request.new_context()
    response = context.get(url=f"https://hr-challenge.dev.tapyou.com/api/test/users?gender={user_gender}")
    data = response.json()

    assert data['error'] == "Internal Server Error"
    assert response.status == 500, f"Expected status code 500, actually got {response.status}"
    assert response.status_text == "Internal Server Error", f"Expected status text 'Internal Server Error', actually got '{response.status_text}'"
    assert response.headers['content-type'] == 'application/json;charset=UTF-8'