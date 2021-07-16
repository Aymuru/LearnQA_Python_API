import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegistry(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        check_email = self.prepare_registration_data()['email']
        Assertions.assert_no_add_symbol_in_email(check_email, "@")

    def test_create_user_empty_fields(self):
        data = {
            'password': None,
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': None,
            'email': self.prepare_registration_data()['email']
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_wrong_data(response)

    def test_short_firstName(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': '',
            'lastName': 'learnqa',
            'email': self.prepare_registration_data()['email']
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_short_name(response, data['firstName'])

    def test_long_firstName(self):
        a = ['a' for i in range(251)]
        long_name = ''.join(a)

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': long_name,
            'lastName': 'learnqa',
            'email': self.prepare_registration_data()['email']
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_long_name(response, data['firstName'])

