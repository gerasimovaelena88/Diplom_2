import pytest
import allure
import random
import string
import requests
from api.api_client import ApiClient


@pytest.fixture
@allure.step("Инициализация API клиента")
def api_client():
    """Фикстура для создания экземпляра API клиента"""
    return ApiClient()

@pytest.fixture
def random_user_data():
    """Генерирует случайные данные пользователя для тестов"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"test_user_{random_string}@example.com"
    password = "TestPassword123"
    name = f"Test User {random_string}"
    
    return {
        "email": email,
        "password": password,
        "name": name
    }

@pytest.fixture
def registered_user(api_client, random_user_data):
    """Фикстура для создания и удаления тестового пользователя"""
    # Регистрация пользователя
    response = api_client.create_user(
        random_user_data["email"],
        random_user_data["password"],
        random_user_data["name"]
    )
    
    assert response.status_code == 200, f"Failed to register user: {response.text}"
    
    user_data = response.json()
    token = user_data.get('accessToken')
    
    # Очищаем токен от 'Bearer ' если он есть
    if token and token.startswith('Bearer '):
        token = token[7:]
    
    yield {
        "email": random_user_data["email"],
        "password": random_user_data["password"],
        "name": random_user_data["name"],
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
