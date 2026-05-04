import allure
import jsonschema
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature ("Pet")

class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"}
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet" , json=payload)
            response_json = response.json()

        with allure.step("Проверка стастатуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_full_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"}

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка стастатуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя  питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "ссылка на питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "теги на питомца не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id (self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet ['id']

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()['id'] == pet_id



    @allure.title("Обновление информации о питомце")
    def test_put_pet(self, create_pet):
        pet_id = create_pet['id']

        # Подготовка данных для обновления
        update_payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold"
        }

        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(url=f"{BASE_URL}/pet",json=update_payload)

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()['name'] == "Buddy Updated"
            assert response.json()['status'] == "sold"

    @allure.title("Удаление питомца по ID")
    def test_deleted_pet_by_id(self, create_pet):
        pet_id = create_pet['id']

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet")
            response_json = response.json()


        with allure.step("Отправка запроса на удаление информации о питомце"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")


        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        assert get_response.status_code == 404, "Питомец всё еще существует после удаления"


