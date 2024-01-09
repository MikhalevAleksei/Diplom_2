import pytest
import requests
from faker import Faker

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls

fake = Faker(locale="ru_RU")


@pytest.fixture
def user_registration():
    payload = {}
    user = fake_user()
    payload["email"] = user["email"]
    payload["password"] = user["password"]
    payload["name"] = user["name"]
    requests.post(
        f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
        data=payload)


@pytest.fixture()
def fixture_to_parametrize():
    fake_login = fake_user()
    name = fake_login['name']

    return name


@pytest.fixture()
def make_order(user_registration):
    ingredient_hash_data = {
        "ingredients": ["60d3b41abdacab0026a733c6",
                        "609646e4dc916e00276b2870"]
    }
    requests.post(
        f'{Urls.MAIN_URL}{Handlers.MAKE_ORDER}', data=ingredient_hash_data)


