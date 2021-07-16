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
