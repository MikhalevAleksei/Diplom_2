import allure
import pytest
import requests

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls


class TestAuthorisation:
    data = {}

    def setup_class(self):
        user = fake_user()
        self.data["email"] = user["email"]
        self.data["password"] = user["password"]
        self.data["name"] = user["name"]

        self.pytestmark = [pytest.mark.parametrize(
            'email,password', [(self.data["email"], self.data["password"])])]

    @allure.title('Positive login')
    def test_positive_authorisation(self):
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.LOGIN}',
            data=TestAuthorisation.data)
        assert response.status_code == 200

    @allure.title('Login with incorrect data')
    @pytest.mark.parametrize('name', [
        pytest.lazy_fixture('fixture_to_parametrize')])
    def test_negative_login(self, user_registration, email, password, name):
        login_with_incorrect_data = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.LOGIN}',
            data=login_with_incorrect_data)
        assert response.status_code == 401, 'Wrong status code'
        assert response.json()['success'] == False, 'Correct success status'
        assert response.json()['message'] == \
               'email or password are incorrects', 'Incorrect message'

    def teardown_class(self):
        requests.delete(
            f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
            data=TestAuthorisation.data
        )
        self.data.clear()
