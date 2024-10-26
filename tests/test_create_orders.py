from utilities.order_helper import generate_user_data, empty_ingredients
from utilities.order_helper import valid_ingredients, invalid_ingredients
from utilities.urls import DataUrls
import allure


class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией')
    @allure.description('Тест проверяет создание заказа авторизованным пользователем с валидными ингредиентами')
    def test_create_order_with_authorization(self, session):
        with allure.step("Генерация нового пользователя"):
            user = generate_user_data()

        with allure.step("Создание нового пользователя"):
            create_response = session.post(DataUrls.CREATE_USER_URL, json=user)
            assert create_response.status_code == 200

        with allure.step("Авторизация пользователя и получение токена"):
            login_response = session.post(DataUrls.LOGIN_URL, json=user)
            assert login_response.status_code == 200
            access_token = login_response.json().get("accessToken")
            assert access_token

        with allure.step("Создание заказа с валидными ингредиентами"):
            order_payload = valid_ingredients
            response = session.post(DataUrls.ORDERS_URL, headers={"Authorization": access_token}, json=order_payload)
            assert response.status_code == 200

    @allure.title('Создание заказа без авторизации')
    @allure.description('Тест проверяет создание заказа без авторизации, что должно вернуть ошибку 401')
    def test_create_order_without_authorization(self, session):
        with allure.step("Попытка создания заказа без авторизации"):
            order_payload = valid_ingredients
            response = session.post(DataUrls.ORDERS_URL, json=order_payload)
            assert response.status_code == 401

    @allure.title('Создание заказа с невалидным ингредиентом')
    @allure.description('Тест проверяет, что при создании заказа с невалидным ингредиентом возвращается ошибка 500')
    def test_create_order_with_invalid_ingredient(self, session):
        with allure.step("Генерация нового пользователя"):
            user = generate_user_data()

        with allure.step("Создание нового пользователя"):
            session.post(DataUrls.CREATE_USER_URL, json=user)

        with allure.step("Авторизация пользователя и получение токена"):
            session.post(DataUrls.LOGIN_URL, json=user)

        with allure.step("Создание заказа с невалидным ингредиентом"):
            order_payload = invalid_ingredients
            response = session.post(DataUrls.ORDERS_URL, json=order_payload)
            assert response.status_code == 500

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Тест проверяет, что создание заказа без ингредиентов возвращает ошибку 400')
    def test_create_order_without_ingredients(self, session):
        with allure.step("Генерация нового пользователя"):
            user = generate_user_data()

        with allure.step("Создание нового пользователя"):
            session.post(DataUrls.CREATE_USER_URL, json=user)

        with allure.step("Авторизация пользователя"):
            login_response = session.post(DataUrls.LOGIN_URL, json=user)
            access_token = login_response.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Создание заказа без ингредиентов"):
            response = session.post(DataUrls.ORDERS_URL, headers=headers, json=empty_ingredients)
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"
