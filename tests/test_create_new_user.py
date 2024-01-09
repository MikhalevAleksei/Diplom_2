import allure
import pytest
import requests

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls


class TestCreateNewUser:
    data = {}
    user = fake_user()
    PARAM_EMAIL = user["email"]
    PARAM_PASSWORD = user["password"]
    PARAM_NAME = user["name"]

    def setup_class(self):
        user = fake_user()
        self.data["email"] = user["email"]
        self.data["password"] = user["password"]
        self.data["name"] = user["name"]

    @allure.title('create new  user')
    def test_create_new_user(self):
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            data=TestCreateNewUser.data)
        assert response.status_code == 200

    @allure.title('create existing user')
    def test_create_existing_user(self):
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            data=TestCreateNewUser.data)
        assert response.status_code == 403, 'Wrong status code'
        assert response.json()['success'] == False, 'Wrong success status'
        assert response.json()['message'] == 'User already exists', 'Wrong ' \
                                                                    'message'

    @allure.title('create user without all fields')
    @pytest.mark.parametrize('email, password, name',
                             [
                                 (
                                         PARAM_EMAIL,
                                         PARAM_PASSWORD,
                                         '',
                                 ),
                                 (
                                         PARAM_EMAIL,
                                         '',
                                         PARAM_NAME,
                                 ),
                                 (
                                         '',
                                         PARAM_PASSWORD,
                                         PARAM_NAME
                                 )
                             ])
    def test_create_existing_user(self, email, password, name):
        create_user_without_one_fild = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            data=create_user_without_one_fild)
        assert response.status_code == 403, 'Wrong status code'
        assert response.json()['success'] == False, 'Incorrect success status'
        assert response.json()['message'] == \
               'Email, password and name are required fields', \
            'Incorrect message'

    def teardown_class(self):
        requests.delete(
            f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
            data=TestCreateNewUser.data
        )
        self.data.clear()

