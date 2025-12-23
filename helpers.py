import random
import string


def generate_random_user_data():
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
