import allure
import pytest
import requests

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls


class TestChangeUserData:
    PATCH_EMAIL = {
        'email': 'patchnewmail@mail.com'
    }
    PATCH_NAME = {
        'name': 'some_name'
    }
    data = {}

    def setup_class(self):
        user = fake_user()
        self.data["email"] = user["email"]
        self.data["password"] = user["password"]
        self.data["name"] = user["name"]

    @allure.title('Test user personal data')
    @pytest.mark.parametrize('patch_data', [PATCH_EMAIL, PATCH_NAME])
    def test_change_user_data(self, patch_data):
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            data=TestChangeUserData.data)
        data_before_patch = response.text
        token = response.json()['authorisation']

        response_patch = requests.patch(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            params=patch_data, headers=token)
        data_after_patch = response_patch.text

        assert data_before_patch != data_after_patch, 'Data hasn`t changed'
        assert response.json()['success'] == True, 'No success status'

    @allure.title('Test change personal data without authorisation')
    def test_change_data_without_authorisation(self):
        try_change_email = 'negativepatchmail@mail.com'
        patch_data = {
            'email': try_change_email
        }
        response = requests.patch(
            f'{Urls.MAIN_URL}{Handlers.CREATE_USER}',
            params=patch_data)

        assert response.status_code == 401, 'User has authorisation'
        assert response.json()['success'] == False, 'Success status'
        assert response.json()['message'] == \
               'You should be authorised', 'Incorrect message'

    def teardown_class(self):
        requests.delete(
            f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
            data=TestChangeUserData.data
        )
        self.data.clear()


