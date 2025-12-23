import pytest
import allure
import requests
from api.api_client import ApiClient
from helpers import generate_random_user_data


@pytest.fixture
@allure.step("Инициализация API клиента")
def api_client():
    """Фикстура для создания экземпляра API клиента"""
    return ApiClient()

@pytest.fixture
def registered_user(api_client):
    """Фикстура для создания и удаления тестового пользователя"""

    # Генерируем данные напрямую через функцию
    user_data = generate_random_user_data()

    # Регистрация пользователя
    response = api_client.create_user(
        user_data["email"],
        user_data["password"],
        user_data["name"]
    )
    
    assert response.status_code == 200, f"Failed to register user: {response.text}"
    
    response_data = response.json()
    token = response_data.get('accessToken')
    
    # Очищаем токен от 'Bearer ' если он есть
    if token and token.startswith('Bearer '):
        token = token[7:]
    
    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "token": token
    }
    
    # Очистка - удаление пользователя после теста
    if token:
        api_client.delete_user(token)

@pytest.fixture
@allure.step("Получение списка ингредиентов")
def get_ingredients(api_client):
    """Фикстура для получения доступных ингредиентов"""
    response = api_client.get_ingredients()
    assert response.status_code == 200, "Failed to get ingredients"
    
    ingredients_data = response.json()
    return ingredients_data.get('data', [])
