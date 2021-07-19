import time
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("User editing cases")
@allure.feature("Кейсы редактирования")
class TestUserEdit(BaseCase):

    @allure.title("Успешное редактирование только что созданного юзера")
    @allure.description("Создали юзера и им же изменили имя на другое")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user(self):
        # REGISTER
        with allure.step("Создаем пользователя"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step("Авторизовываемся пользователем"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        with allure.step(f"Меняем имя пользователя на новое - {new_name}"):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step(f"Проверяем что изначальное имя ({first_name}) изменилось на новое ({new_name})"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of user after edit"
            )

    @allure.title("Редактирование неавторизованного юзера")
    @allure.description("Проверка на то, что нельзя редактировать данные неавторизованного юзера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_not_auth_user(self):
        # REGISTER
        with allure.step("Создаем пользователя"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        # EDIT
        new_pas = "Changed Password"
        with allure.step(f"Пытаемся изменить изначальный пароль ({password}) на новый ({new_pas})"):
            response2 = MyRequests.put(
                f"/user/{user_id}",
                data={"password": new_pas}
            )
            Assertions.assert_change_data_of_not_auth_user(response2)

    @allure.title("Редактирование одного пользователя другим")
    @allure.description("Проверка на то, что нельзя редактировать данные другого юзера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_by_different_user(self):
        # REGISTERING USER 1
        with allure.step("Создаем первого юзера"):
            user1 = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=user1)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")

        time.sleep(0.5)

        # REGISTERING AND LOGIN IN USER 2
        with allure.step("Создаем второго юзера"):
            user2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=user2)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

        with allure.step("Авторизовываемся под вторым юзером"):
            response3 = MyRequests.post("/user/login", data=user2)
            auth_sid2 = self.get_cookie(response3, "auth_sid")
            token2 = self.get_header(response3, "x-csrf-token")

        # USER 2 TRIES TO EDIT USER 1
        new_username = "Changed USERNAME LIKE A BOSS"
        with allure.step(f"Пытаемся изменить имя юзера на новое - {new_username} будучи авторизованным за другого юзера"):
            response4 = MyRequests.put(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid2},
                headers={"x-csrf-token": token2},
                data={"username": new_username}
            )

        # USER 1 AUTHORIZING AND GETTING INFO ABOUT HIMSELF
        with allure.step("Авторизовываемся первым юзером"):
            response5 = MyRequests.post("/user/login", data=user1)
            auth_sid1 = self.get_cookie(response5, "auth_sid")
            token1 = self.get_header(response5, "x-csrf-token")

        with allure.step("Проверяем изменилось ли изначальное имя на новое"):
            response6 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid1},
                headers={"x-csrf-token": token1}
            )

            # COMPARE PREVIOUS 'USERNAME' OF USER 1 WITH EXPECTING CHANGED DATA
            username1 = response6.json()['username']
            Assertions.assert_change_data_by_different_user(response4, username1, new_username)

    @allure.title("Изменение email на новый без @")
    @allure.description("Почта не может быть создана или изменена на новую без символа @")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_email_without_add_symbol(self):
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
        with allure.step("Авторизовываемся за пользователя"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EMAIL BEFORE PUT METHOD
        with allure.step("Проверяем чему равно поле email"):
            response6 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )
            print("Email BEFORE PUT method - ", response6.json()['email'])

        # EDIT
        new_mail = email.replace("@", "")
        with allure.step("Изменяем email на новый без символа @"):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_mail}
            )

        # EMAIL AFTER PUT METHOD
        with allure.step("Проверяем чему равно поле email"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )
            print("Email AFTER PUT method - ", response4.json()['email'])

            Assertions.assert_change_into_wrong_email(response3)

    @allure.title("Изменение имени на новое короткое")
    @allure.description("Имя не может быть создано или изменено на новое длиной меньше 1 символа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_into_short_firstname(self):
        # REGISTER
        with allure.step("Создаем пользователя"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            name = register_data['firstName']
            user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step("Авторизовываемся за пользователя"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # FIRSTNAME BEFORE PUT METHOD
        with allure.step("Проверяем чему равно поле имени"):
            response6 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )
            print("FirstName BEFORE PUT method - ", response6.json()['firstName'])

        # EDIT
        new_name = name.replace(name, "")
        with allure.step("Изменяем имя на новое длиной 0-1 символа"):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

        # FirstName AFTER PUT METHOD
        with allure.step("Проверяем чему равно поле имени"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )
            print("FirstName AFTER PUT method - ", response4.json()['firstName'])

            Assertions.assert_change_into_short_name(response3, new_name)

