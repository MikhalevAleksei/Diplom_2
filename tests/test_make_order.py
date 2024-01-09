import allure
import requests

from handlers import Handlers
from helpers import make_new_fake_user_and_return_data as fake_user
from urls import Urls


class TestMakeOrder:
    data = {}

    def setup_class(self):
        user = fake_user()
        self.data["email"] = user["email"]
        self.data["password"] = user["password"]
        self.data["name"] = user["name"]

    @allure.title('Test make order with registration and with ingredients')
    def test_make_order_with_registration_and_ingredients(self,
                                                          user_registration):
        ingredient_hash_data = {
            "ingredients": ["60d3b41abdacab0026a733c6",
                            "609646e4dc916e00276b2870"]
        }
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.MAKE_ORDER}', data=ingredient_hash_data)
        assert response.status_code == 200
        assert response.json()['success'] == True

    @allure.title('Test make order without registration')
    def test_make_order_without_registration(self, user_registration):
        ingredient_hash_data = {
            "ingredients": ["60d3b41abdacab0026a733c6",
                            "609646e4dc916e00276b2870"]
        }
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.MAKE_ORDER}', data=ingredient_hash_data)
        assert response.json()['success'] == False

    @allure.title('Test make order with registration and without ingredients')
    def test_make_order_without_ingredients(self, user_registration):
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.MAKE_ORDER}')
        assert response.status_code == 400
        assert response.json()['success'] == False, 'Order has made without ' \
                                                    'ingredients'

    @allure.title('Test make order with incorrect hash of ingredients')
    def test_make_order_with_wrong_hash(self, user_registration):
        ingredient_hash_data = {
            "ingredients": ["60d3b41abdacab0026a733c6wrong",
                            "609646e4dc916e00276b2870incorrect"]
        }
        response = requests.post(
            f'{Urls.MAIN_URL}{Handlers.MAKE_ORDER}', data=ingredient_hash_data)
        assert response.status_code == 400
        assert response.json()['success'] == False, 'Order has made with ' \
                                                    'incorrect hash of ' \
                                                    'ingredients'

    def teardown_class(self):
        requests.delete(
            f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
            data=TestMakeOrder.data
        )
        self.data.clear()

