from lib.my_requests import MyRequests
import time
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_locked_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            "/user/2",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_delete_locked_user(response2)

    def test_delete_new_user(self):
        # REGISTER
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

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # CHECK OF USER EXISTENCE
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # DELETE
        response4 = MyRequests.delete(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        # CHECK OF USER EXISTENCE
        response5 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_delete_user(response5)

    def test_delete_different_user(self):
        # REGISTERING USER 1
        user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        time.sleep(0.5)

        # REGISTERING AND LOGIN IN USER 2
        user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        response3 = MyRequests.post("/user/login", data=user2)
        auth_sid2 = self.get_cookie(response3, "auth_sid")
        token2 = self.get_header(response3, "x-csrf-token")

        # USER 2 TRIES TO DELETE USER 1

        response4 = MyRequests.delete(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid2},
            headers={"x-csrf-token": token2}
        )

        response6 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_delete_user_by_different_one(response6)
