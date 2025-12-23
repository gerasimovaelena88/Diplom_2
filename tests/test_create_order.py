import pytest
import allure


@allure.feature("Создание заказов")
@allure.story("Тестирование функционала создания заказов")
class TestCreateOrder:
    
    @pytest.mark.parametrize(
        "ingredients_count",
        [1, 2]
    )
    @allure.title("Успешное создание заказа с {ingredients_count} ингредиентом(ами)")
    def test_create_order_with_different_ingredient_counts(
        self, api_client, registered_user, get_ingredients, ingredients_count):
        """Параметризованный тест для проверки создания заказа с разным количеством ингредиентов."""

        with allure.step("Авторизация пользователя"):
            api_client.login_user(registered_user["email"], registered_user["password"])
        
        with allure.step("Получение ингредиентов"):
            ingredients = get_ingredients
            if len(ingredients) < ingredients_count:
                pytest.skip(f"Need at least {ingredients_count} ingredients for test")
        
        with allure.step(f"Создание заказа с {ingredients_count} ингредиентом(ами)"):
            # Берем нужное количество ингредиентов
            ingredient_ids = [ingredients[i]["_id"] for i in range(ingredients_count)]
            response = api_client.create_order(ingredient_ids, auth=True)
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert "order" in data

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет создание заказа без авторизации пользователя")
    def test_create_order_without_auth(self, api_client, get_ingredients):
        """
        Тест проверяет что неавторизованный пользователь НЕ может создать заказ.
        Ожидаемый результат: 401 Unauthorized
        """
        with allure.step("Получение ингредиентов"):
            ingredients = get_ingredients
            if not ingredients:
                pytest.skip("No ingredients available")
        
        with allure.step("Создание заказа без авторизации"):    
            ingredient_ids = [ingredients[0]["_id"]]
            response = api_client.create_order(ingredient_ids, auth=False)
            
            # Однозначный ожидаемый результат
            assert response.status_code == 401, f"Expected 401 for unauthorized order, got {response.status_code}"
            
            data = response.json()
            assert data["success"] is False
            assert "message" in data  # Проверяем наличие сообщения об ошибке
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Тест проверяет создание заказа без указания ингредиентов")
    def test_create_order_without_ingredients(self, api_client, registered_user):
        with allure.step("Авторизация пользователя"):
            api_client.login_user(registered_user["email"], registered_user["password"])

        with allure.step("Создание заказа без ингредиентов"):    
            response = api_client.create_order([], auth=True)
            
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
    
    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    @allure.description("Тест проверяет обработку невалидных идентификаторов ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, api_client, registered_user):
        """
        Тест проверяет обработку невалидных идентификаторов ингредиентов.
        Согласно документации: ожидается 500 Internal Server Error.
        """
        with allure.step("Авторизация пользователя"):
            api_client.login_user(registered_user["email"], registered_user["password"])
        
        with allure.step("Создание заказа с невалидными ингредиентами"):
            # Используем явно невалидные хеши
            invalid_ingredients = ["invalid_hash_123", "invalid_hash_456"]
            response = api_client.create_order(invalid_ingredients, auth=True)
        
        with allure.step("Проверка ответа согласно документации"):
            # По документации: 500 Internal Server Error
            assert response.status_code == 500, (
                f"Согласно документации ожидался статус 500 для невалидного хеша ингредиентов, "
                f"получен {response.status_code}\n"
                f"Ответ: {response.text[:200]}..."  # Показываем начало ответа
            )
    