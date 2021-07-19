from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Registration cases")
@allure.feature("Кейсы регистрации")
class TestUserRegistry(BaseCase):

    @allure.title("Успешное создание юзера")
    @allure.description("Checking the creation of user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_successfully(self):
        with allure.step("Создаем пользователя"):
            data = self.prepare_registration_data()

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.title("Создание юзера с существующим мылом")
    @allure.description("Checking that we can't create user with existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Создаем пользователя с email = {email}"):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Unexpected response content {response.content}"

    @allure.title("Создание юзера с мылом без @")
    @allure.description("Checking that we can't create user without symbol '@' in email")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_create_user_with_incorrect_email(self):
        with allure.step("Делаем проверку на наличие @ в передаваемом email"):
            check_email = self.prepare_registration_data()['email']
            Assertions.assert_no_add_symbol_in_email(check_email, "@")

    @allure.title("Создание юзера с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Checking that we can't create user without expecting fields")
    def test_create_user_empty_fields(self):
        data = {
            'password': None,
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': None,
            'email': self.prepare_registration_data()['email']
        }
        with allure.step("Создаем пользователя с пустым паролем и фамилией"):
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_wrong_data(response)

    @allure.title("Создание юзера с коротким именем")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.description("The name of user can't be less than 1 symbol")
    def test_short_firstName(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': '',
            'lastName': 'learnqa',
            'email': self.prepare_registration_data()['email']
        }
        with allure.step(f"Создаем пользователя с именем - ' {data['firstName']} '"):
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_short_name(response, data['firstName'])

    @allure.title("Создание юзера с длинным именем")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.description("The name of user can't be more than 250 symbols")
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
        with allure.step(f"Создаем пользователя с именем {long_name}"):
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_long_name(response, data['firstName'])
