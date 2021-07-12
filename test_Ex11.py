import requests


class TestCheckCookie:
    def test_cookie_check(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)

        assert "HomeWork" in response.cookies, "There is no expected cookie in the response"

        cookie = response.cookies.get("HomeWork")
        print(cookie)

        assert cookie == "hw_value", "Cookie is not correct"
