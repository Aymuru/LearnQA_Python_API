import requests


class TestCheckHeader:
    def test_header_check(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)

        assert "x-secret-homework-header" in response.headers, "There is no expected header in the response"

        header = response.headers.get("x-secret-homework-header")
        print(header)

        assert header == "Some secret value", "Header is not correct"
