from utilities.order_helper import generate_user_data
from utilities.urls import DataUrls
from utilities.order_helper import valid_ingredients
import allure


class TestReceivingOrders:
    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('Тест проверяет получение заказов для авторизованного пользователя')
    def test_receiving_orders_with_authorization(self, session):
        with allure.step("Генерация нового пользователя"):
            user = generate_user_data()

        with allure.step("Создание нового пользователя"):
            create_response = session.post(DataUrls.CREATE_USER_URL, json=user)
            assert create_response.status_code == 200

        with allure.step("Авторизация пользователя и получение токена"):
            login_response = session.post(DataUrls.LOGIN_URL, json={
                "email": user["email"],
                "password": user["password"]
            })
            assert login_response.status_code == 200
            access_token = login_response.json().get("accessToken")
            assert access_token

        with allure.step("Создание заказа с валидными ингредиентами"):
            order_payload = valid_ingredients
            create_order_response = session.post(DataUrls.ORDERS_URL, headers={"Authorization": access_token},
                                                 json=order_payload)
            assert create_order_response.status_code == 200

        with allure.step("Получение заказов пользователя"):
            orders_response = session.get(DataUrls.ORDERS_URL, headers={"Authorization": access_token})
            assert orders_response.status_code == 200
            assert orders_response.json().get("orders")

        with allure.step('Удаление пользователя после завершения теста'):
            delete_response = session.delete(DataUrls.USER_URL, headers={"Authorization": access_token})
            assert delete_response.status_code in [200, 202]

    @allure.title('Получение заказов без авторизации')
    @allure.description('Тест проверяет, что при получении заказов без авторизации возвращается ошибка 401')
    def test_receiving_orders_without_authorization(self, session):
        orders_response = session.get(DataUrls.ORDERS_URL)

        assert orders_response.status_code == 401
        assert orders_response.json().get("message") == "You should be authorised"
