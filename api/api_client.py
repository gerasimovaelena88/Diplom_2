import allure
import requests
import logging
from .endpoints import REGISTER, LOGIN, USER, ORDERS, INGREDIENTS


class ApiClient:
    def __init__(self):
        """Инициализация клиента API с сессией для сохранения состояния"""
        self.session = requests.Session() # Сессия для сохранения состояния между запросами
        self.token = None # Токен авторизации
    
    def _clean_token(self, token):
        """Удаляет префикс 'Bearer ' из токена, если он присутствует"""
        if token and token.startswith('Bearer '):
            return token[7:]  # Удаляем 'Bearer ' из начала строки
        return token
    
    def _get_headers(self, auth=True):
        """Возвращает заголовки для HTTP запроса с опциональной авторизацией"""
        headers = {'Content-Type': 'application/json'}
        if auth and self.token:
            # Очищаем токен от 'Bearer ' перед добавлением в заголовок
            clean_token = self._clean_token(self.token)
            headers['Authorization'] = f'Bearer {clean_token}'
        return headers
    
    @allure.step("Создание пользователя: {email}")
    def create_user(self, email, password, name):
        """Создает нового пользователя в системе"""
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return self.session.post(REGISTER, json=payload)
    
    @allure.step("Авторизация пользователя: {email}")
    def login_user(self, email, password):
        """Выполняет вход пользователя в систему"""
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(LOGIN, json=payload)
        
        if response.status_code == 200:
            # Получаем токен из ответа и сохраняем его
            self.token = response.json().get('accessToken')
            # Очищаем токен от префикса 'Bearer ' при сохранении
            self.token = self._clean_token(self.token)
        
        return response
    
    @allure.step("Создание заказа с ингредиентами: {ingredients}")
    def create_order(self, ingredients, auth=True):
        """Создает заказ с указанными ингредиентами"""
        payload = {"ingredients": ingredients}
        headers = self._get_headers(auth)
        
        return requests.post(ORDERS, json=payload, headers=headers)
    
    @allure.step("Получение списка доступных ингредиентов")
    def get_ingredients(self):
        """Получает список всех доступных ингредиентов"""
        return requests.get(INGREDIENTS)
    
    @allure.step("Удаление пользователя")
    def delete_user(self, token=None):
        """Удаляет пользователя (используется для очистки тестовых данных)"""
        # Используем переданный токен или токен из текущей сессии
        delete_token = token or self.token
        if delete_token:
            # Очищаем токен перед использованием
            clean_token = self._clean_token(delete_token)
            headers = {'Authorization': f'Bearer {clean_token}'}
            return requests.delete(USER, headers=headers)
        return None
    