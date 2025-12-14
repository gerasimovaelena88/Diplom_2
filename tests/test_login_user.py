import pytest
import allure


@allure.feature("Авторизация пользователя")
@allure.story("Тестирование функционала входа в систему")
class TestLoginUser:
    
    @allure.title("Успешная авторизация существующего пользователя")
    @allure.description("Тест проверяет успешный вход в систему с правильными учетными данными")
    def test_login_existing_user_success(self, api_client, registered_user):
        with allure.step("Авторизация с корректными данными"):
            response = api_client.login_user(
                registered_user["email"],
                registered_user["password"]
            )
        with allure.step("Проверка ответа"):    
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "accessToken" in data
    
    @allure.title("Авторизация с неверным email")
    @allure.description("Тест проверяет попытку входа с несуществующим email")
    def test_login_with_wrong_email(self, api_client, registered_user):
        with allure.step("Авторизация с неверным email"):
            response = api_client.login_user(
                "wrong_email@example.com",
                registered_user["password"]
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert "email or password are incorrect" in data["message"]
    
    @allure.title("Авторизация с неверным паролем")
    @allure.description("Тест проверяет попытку входа с неправильным паролем")
    def test_login_with_wrong_password(self, api_client, registered_user):
        with allure.step("Авторизация с неверным паролем"):
            response = api_client.login_user(
                registered_user["email"],
                "WrongPassword123"
            )

        with allure.step("Проверка ответа"):    
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert "email or password are incorrect" in data["message"]
