from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Cases of getting info")
@allure.feature("Кейсы запроса данных пользователя")
class TestUserGet(BaseCase):

    @allure.title("Запрос данных неавторизованного юзера")
    @allure.description("Нельзя удалять или редактировать юзеров неавторизованной зоны")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_not_auth(self):
        with allure.step("Запрос данных пользователя с id 2"):
            response = MyRequests.get("/user/2")

            Assertions.assert_json_has_key(response, "username")

            expected_fields1 = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_no_keys(response, expected_fields1)

    @allure.title("Запрос данных авторизованного юзера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Авторизация юзера с email = {data['email']}"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Запрос данных юзера"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields2 = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields2)

    @allure.title("Запрос данных юзера другим юзером")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_different_user(self):

        # авторизованный пользователь
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Авторизация юзера с email = {data['email']}"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        # Создание нового пользователя
        data2 = self.prepare_registration_data()
        with allure.step("Создаем нового юзера"):
            response2 = MyRequests.post("/user/", data=data2)
            user2_id = self.get_json_value(response2, "id")

        # Передача куки и токена авторизованного юзера в новозарегистрированного
        with allure.step("Пытаемся запросить данные созданного юзера авторизованным"):
            response3 = MyRequests.get(
                f"/user/{user2_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            expected_fields = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_key(response3, "username")
            Assertions.assert_json_has_no_keys(response3, expected_fields)