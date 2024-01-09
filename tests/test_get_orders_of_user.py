import allure
import requests

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls


class TestGetOrdersOfUser:
    data = {}

    def setup_class(self):
        user = fake_user()
        self.data["email"] = user["email"]
        self.data["password"] = user["password"]
        self.data["name"] = user["name"]

    @allure.title('Test get orders with authorisation')
    def test_get_orders_of_user(self, user_registration, make_order):
        get_response = requests.get(
            f'{Urls.MAIN_URL}{Handlers.GET_ORDERS}')

        assert get_response.status_code == 200
        assert get_response.json()['success'] == True

    def test_get_orders_of_user_without_authorisation(self):
        get_response = requests.get(
            f'{Urls.MAIN_URL}{Handlers.GET_ORDERS}')

        assert get_response.status_code == 400
        assert get_response.json()['success'] == False, 'Have got orders of ' \
                                                        'user without ' \
                                                        'authentication'

    def teardown_class(self):
        requests.delete(
            f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
            data=TestGetOrdersOfUser.data
        )
        self.data.clear()
