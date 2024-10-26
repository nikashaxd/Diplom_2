import pytest
from utilities.urls import DataUrls
from utilities.generator_data import generate_random_string
import allure


class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    @allure.description('Тест проверяет создание уникального пользователя')
    def test_create_unique_user(self, session):
        payload = {
            "email": f"{generate_random_string(8)}@yandex.ru",
            "password": generate_random_string(10),
            "name": generate_random_string(8)
        }
        response = session.post(DataUrls.CREATE_USER_URL, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True

        with allure.step('Получаем токен пользователя для его удаления'):
            access_token = response.json()["accessToken"]
            headers = {"Authorization": access_token}

        with allure.step('Используем правильный URL для удаления пользователя'):
            delete_response = session.delete(DataUrls.USER_URL, headers=headers)
            assert delete_response.status_code in [200, 202]  # Учитываем возможный статус 202 Accepted

    @allure.title('Создание уже существующего пользователя')
    @allure.description('Тест проверяет, что при создании уже существующего пользователя возращается ошибка 403')
    def test_create_existing_user(self, session):
        payload = {
            "email": "existing_user@yandex.ru",
            "password": generate_random_string(10),
            "name": generate_random_string(8)
        }
        response = session.post(DataUrls.CREATE_USER_URL, json=payload)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title('Создание пользователя с пропущенным полем')
    @allure.description('Тест проверяет, что при пропущенном обязательном поле возвращается ошибка 403')
    @pytest.mark.parametrize("payload, missing_field", [
        ({"password": generate_random_string(10), "name": generate_random_string(8)}, "email"),  # Пропущено поле email
        ({"email": f"{generate_random_string(8)}@yandex.ru", "name": generate_random_string(8)}, "password"),
        # Пропущено поле password
        ({"email": f"{generate_random_string(8)}@yandex.ru", "password": generate_random_string(10)}, "name")
        # Пропущено поле name
    ])
    def test_create_user_missing_fields(self, session, payload, missing_field):
        response = session.post(DataUrls.CREATE_USER_URL, json=payload)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
