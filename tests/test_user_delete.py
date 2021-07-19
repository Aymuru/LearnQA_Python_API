from lib.my_requests import MyRequests
import time
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Cases of deleting")
@allure.label("DELETION", "desktop")
@allure.feature("Кейсы удаления")
class TestUserDelete(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Удаление залоченного юзера")
    @allure.description("Нельзя удалять или редактировать юзеров с id 1-5")
    def test_delete_locked_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step(f"Авторизовываемся за пользователя с данными {data}"):
            response1 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step("Пытаемся удалить пользователя, который не может быть удален"):
            response2 = MyRequests.delete(
                "/user/2",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )

        Assertions.assert_delete_locked_user(response2)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание и удаление юзера")
    def test_delete_new_user(self):
        # REGISTER
        with allure.step("Создаем пользователя"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']

            user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step(f"Авторизовываемся за пользователя c данными {login_data}"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # CHECK OF USER EXISTENCE
        with allure.step(f"Проверяем, что юзер с данными {login_data} существует"):
            response3 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        # DELETE
        with allure.step(f"Удаляем юзера с данными {login_data}"):
            response4 = MyRequests.delete(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )

        # CHECK OF USER EXISTENCE
        with allure.step(f"Проверяем, что юзер с данными {login_data} был удален"):
            response5 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_delete_user(response5)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление одного юзера другим")
    def test_delete_different_user(self):
        # REGISTERING USER 1
        with allure.step("Создаем первого пользователя"):
            user1 = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=user1)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")

        time.sleep(0.5)

        # REGISTERING AND LOGIN IN USER 2
        with allure.step("Создаем второго пользователя"):
            user2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=user2)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

        with allure.step("Авторизовываемся под вторым пользователем"):
            response3 = MyRequests.post("/user/login", data=user2)
            auth_sid2 = self.get_cookie(response3, "auth_sid")
            token2 = self.get_header(response3, "x-csrf-token")
            user_id2 = self.get_json_value(response2, "id")

        # USER 2 TRIES TO DELETE USER 1
        with allure.step(f"Пытаемся вторым пользователем (id {user_id2}) удалить первого пользователя с id {user_id}"):
            response4 = MyRequests.delete(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid2},
                headers={"x-csrf-token": token2}
            )

        with allure.step(f"Проверяем что пользователь с id {user_id} все еще существует"):
            response6 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_delete_user_by_different_one(response6)
