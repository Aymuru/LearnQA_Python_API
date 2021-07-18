import time

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

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

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of user after edit"
        )

    def test_edit_not_auth_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_pas = "Changed Password"

        response2 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            data={"password": new_pas}
        )
        Assertions.assert_change_data_of_not_auth_user(response2)

    def test_edit_by_different_user(self):
        # REGISTERING USER 1
        user1 = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=user1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        time.sleep(0.5)

        # REGISTERING AND LOGIN IN USER 2
        user2 = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=user2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=user2)
        auth_sid2 = self.get_cookie(response3, "auth_sid")
        token2 = self.get_header(response3, "x-csrf-token")

        # USER 2 TRIES TO EDIT USER 1
        new_username = "Changed USERNAME LIKE A BOSS"

        response4 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid2},
            headers={"x-csrf-token": token2},
            data={"username": new_username}
        )

        # USER 1 AUTHORIZING AND GETTING INFO ABOUT HIMSELF
        response5 = requests.post("https://playground.learnqa.ru/api/user/login", data=user1)
        auth_sid1 = self.get_cookie(response5, "auth_sid")
        token1 = self.get_header(response5, "x-csrf-token")

        response6 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid1},
            headers={"x-csrf-token": token1}
        )

        # COMPARE PREVIOUS 'USERNAME' OF USER 1 WITH EXPECTING CHANGED DATA
        username1 = response6.json()['username']
        Assertions.assert_change_data_by_different_user(response4, username1, new_username)

    def test_edit_email_without_add_symbol(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

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
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EMAIL BEFORE PUT METHOD
        response6 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        print("Email BEFORE PUT method - ", response6.json()['email'])

        # EDIT
        new_mail = email.replace("@", "")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_mail}
        )

        # EMAIL AFTER PUT METHOD
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        print("Email AFTER PUT method - ", response4.json()['email'])

        Assertions.assert_change_into_wrong_email(response3)

    def test_edit_into_short_firstname(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

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
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # FIRSTNAME BEFORE PUT METHOD
        response6 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        print("FirstName BEFORE PUT method - ", response6.json()['firstName'])

        # EDIT
        new_name = name.replace(name, "k")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        # FirstName AFTER PUT METHOD
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        print("FirstName AFTER PUT method - ", response4.json()['firstName'])

        Assertions.assert_change_into_short_name(response3, new_name)

