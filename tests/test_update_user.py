from utilities.order_helper import generate_user_data
from utilities.urls import DataUrls
from utilities.generator_data import generate_random_string
import allure


class TestUpdateUser:
    @allure.title('Обновление данных пользователя с авторизацией')
    @allure.description('Тест проверяет успешное обновление данных пользователя при наличии авторизации')
    def test_update_user_authorized(self, session):
        with allure.step("Генерация нового пользователя"):
            user = generate_user_data()

        with allure.step("Создание нового пользователя"):
            create_response = session.post(DataUrls.CREATE_USER_URL, json=user)
            assert create_response.status_code == 200

        with allure.step("Авторизация пользователя"):
            login_response = session.post(DataUrls.LOGIN_URL, json={
                "email": user["email"],
                "password": user["password"]
            })
            assert login_response.status_code == 200

            access_token = login_response.json().get("accessToken")
            assert access_token

            headers = {"Authorization": access_token}

        with allure.step("Обновление имени пользователя"):
            update_payload = {"name": "UpdatedName"}
            update_response = session.patch(DataUrls.USER_URL, headers=headers, json=update_payload)
            assert update_response.status_code == 200

        with allure.step("Обновление email пользователя"):
            update_payload = {"email": f"{generate_random_string(8)}@yandex.ru"}
            update_response = session.patch(DataUrls.USER_URL, headers=headers, json=update_payload)
            assert update_response.status_code == 200

        with allure.step("Обновление пароля пользователя"):
            update_payload = {"password": generate_random_string(10)}
            update_response = session.patch(DataUrls.USER_URL, headers=headers, json=update_payload)
            assert update_response.status_code == 200

    @allure.title('Обновление данных пользователя без авторизации')
    @allure.description('Тест проверяет, что при обновлении данных без авторизации возвращается ошибка 401')
    def test_update_user_unauthorized(self, session):
        with allure.step("Попытка обновления имени без авторизации"):
            payload = {"name": generate_random_string(8)}
            response = session.patch(DataUrls.USER_URL, json=payload)
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"

        with allure.step("Попытка обновления email без авторизации"):
            payload = {"email": f"{generate_random_string(8)}@yandex.ru"}
            response = session.patch(DataUrls.USER_URL, json=payload)
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"

        with allure.step("Попытка обновления пароль без авторизации"):
            payload = {"password": generate_random_string(10)}
            response = session.patch(DataUrls.USER_URL, json=payload)
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"
