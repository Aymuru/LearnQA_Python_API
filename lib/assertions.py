from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_json_has_no_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_as_dict, f"Response shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_no_add_symbol_in_email(email, symbol):
        assert symbol in email, f"Email doesn't have symbol '{symbol}'"

    @staticmethod
    def assert_wrong_data(response: Response):
        empty_fields = "The following required params are missed:"
        assert empty_fields in response.text, f"The user is created. User id: {response.text} "

    @staticmethod
    def assert_short_name(response: Response, name):
        firstName_field = "The value of 'firstName' field is too short"
        name_len = len(name)
        assert firstName_field in response.text, f"The user is created, name's length = {name_len}, Expected: less than 2 symbols. User id: {response.text} "

    @staticmethod
    def assert_long_name(response: Response, name):
        firstName_field = "The value of 'firstName' field is too long"
        name_len = len(name)
        assert firstName_field in response.text, f"The user is created, name's length = {name_len}, Expected: more than 250 symbols. User id: {response.text} "

    @staticmethod
    def assert_change_data_of_not_auth_user(response: Response):
        change_field = "Auth token not supplied"
        assert change_field in response.text, f"The user is authorized, but token not supplied."

    @staticmethod
    def assert_change_data_by_different_user(response: Response, previous, new):
        assert previous != new, f"Data was changed, but user is not authorized."

    @staticmethod
    def assert_change_into_wrong_email(response: Response):
        invalid_email = "Invalid email format"
        assert invalid_email in response.text, "Email was changed, but has incorrect format"

    @staticmethod
    def assert_change_into_short_name(response: Response, name):
        invalid_name = "Too short value for field firstName"
        name_len = len(name)
        assert invalid_name in response.text, f"FirstName was changed, name's length = {name_len}, Expected: less than 2 symbols."

    @staticmethod
    def assert_delete_locked_user(response: Response):
        error_message = "Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        assert error_message in response.text, f"You have deleted user with 1-5 ID, which has guarding angel!"

    @staticmethod
    def assert_delete_user(response: Response):
        error_message = "User not found"
        assert error_message in response.text, f"The user you've tried to delete - wasn't deleted."

    @staticmethod
    def assert_delete_user_by_different_one(response: Response):
        assert "username" in response.text, f"The user was deleted by other user."