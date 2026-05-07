import allure
import requests
import jsonschema
import pytest
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")

class TestStore:
    @allure.title("Размещение заказа")
    def test_create_store_order(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)

        with allure.step("Проверка статуса ответа и данных"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response.json()["petId"] == payload["petId"], "petId заказа не совпадает с ожидаемым"
            assert response.json()["quantity"] == payload["quantity"], "quantity заказа не совпадает с ожидаемым"
            assert response.json()["status"] == payload["status"], "status заказа не совпадает с ожидаемым"
            assert response.json()["complete"] == payload["complete"], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_store_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            order_Id = 1
            response = requests.get(url=f"{BASE_URL}/store/order/{order_Id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_Id, "ID заказа не совпал с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_store_order_by_id(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_store_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация Json-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, STORE_SCHEMA)