import pytest
import allure
from helpers import generate_random_user_data


@allure.feature("Регистрация пользователя")
@allure.story("Тестирование функционала создания пользователя")
class TestCreateUser:
    
    @allure.title("Успешное создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового уникального пользователя")
    def test_create_unique_user_success(self, api_client):
        with allure.step("Генерация данных пользователя"):
            user_data = generate_random_user_data()

        with allure.step("Создание нового пользователя"):
            response = api_client.create_user(
                user_data["email"],
                user_data["password"],
                user_data["name"]
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "accessToken" in data

        with allure.step("Очистка тестовых данных"):    
            # Удаление созданного пользователя
            api_client.delete_user(data["accessToken"])
    
    @allure.title("Попытка создания существующего пользователя")
    @allure.description("Тест проверяет, что нельзя создать пользователя с уже существующим email")
    def test_create_existing_user_fails(self, api_client, registered_user):
        with allure.step("Попытка создания существующего пользователя"):
            response = api_client.create_user(
                registered_user["email"],
                registered_user["password"],
                registered_user["name"]
            )
            
        with allure.step("Проверка ответа"):    
            assert response.status_code == 403
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "User already exists"
    
    @allure.title("Создание пользователя без email")
    @allure.description("Тест проверяет создание пользователя без указания email")
    def test_create_user_without_email(self, api_client):
        with allure.step("Генерация данных пользователя"):
            user_data = generate_random_user_data()

        with allure.step("Создание пользователя без email"):
            response = api_client.create_user(
                "",
                user_data["password"],
                user_data["name"]
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 403
            assert response.json()["success"] is False
    
    @allure.title("Создание пользователя без пароля")
    @allure.description("Тест проверяет создание пользователя без указания пароля")
    def test_create_user_without_password(self, api_client):
        with allure.step("Генерация данных пользователя"):
            user_data = generate_random_user_data()

        with allure.step("Создание пользователя без пароля"):
            response = api_client.create_user(
                user_data["email"],
                "",
                user_data["name"]
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 403
            assert response.json()["success"] is False
    
    @allure.title("Создание пользователя без имени")
    @allure.description("Тест проверяет создание пользователя без указания имени")
    def test_create_user_without_name(self, api_client):
        with allure.step("Генерация данных пользователя"):
            user_data = generate_random_user_data()

        with allure.step("Создание пользователя без имени"):
            response = api_client.create_user(
                user_data["email"],
                user_data["password"],
                ""
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 403
            assert response.json()["success"] is False
