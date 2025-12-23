# Базовый URL API сервиса Stellar Burgers
BASE_URL = "https://stellarburgers.education-services.ru/api"

# Эндпоинты API
REGISTER = f"{BASE_URL}/auth/register"    # Регистрация нового пользователя
LOGIN = f"{BASE_URL}/auth/login"          # Авторизация пользователя
USER = f"{BASE_URL}/auth/user"            # Операции с пользователем
ORDERS = f"{BASE_URL}/orders"             # Операции с заказами
INGREDIENTS = f"{BASE_URL}/ingredients"   # Получение списка ингредиентов
