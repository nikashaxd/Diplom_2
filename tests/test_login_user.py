import requests
from utilities.urls import DataUrls
from utilities.generator_data import generate_random_string
from utilities.order_helper import generate_user_data
import allure


class TestLoginUser:
    @allure.title('Успешный логин пользователя')
    @allure.description('Тест проверяет успешный логин пользователя')
    def test_login_successful(self, session):
        with allure.step('Генерация данных нового пользователя'):
            user = generate_user_data()

        with allure.step('Создание нового пользователя'):
            create_response = requests.post(DataUrls.CREATE_USER_URL, json=user)
            assert create_response.status_code == 200

        with allure.step('Логин с созданным пользователем'):
            login_response = requests.post(DataUrls.LOGIN_URL, json=user)
            assert login_response.status_code == 200
            assert login_response.json()["success"] is True

        with allure.step('Удаление пользователя после успешного теста'):
            access_token = login_response.json().get("accessToken")
            headers = {"Authorization": access_token}
            delete_response = requests.delete(DataUrls.USER_URL, headers=headers)
            assert delete_response.status_code in [200, 202]

    @allure.title('Логин с неверным паролем')
    @allure.description('Тест проверяет, что при логине с неверным паролем возвращается ошибка 401')
    def test_login_invalid_fields(self, session):
        payload = {
            "email": f"{generate_random_string(8)}@yandex.ru",
            "password": generate_random_string(10)
        }
        response = session.post(DataUrls.LOGIN_URL, json=payload)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
