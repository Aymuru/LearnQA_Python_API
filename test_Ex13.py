import requests
import pytest

class TestUserAgent:
    agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]
    platforms = [
        ("Mobile"),
        ("Mobile"),
        ("Googlebot"),
        ("Web"),
        ("Mobile")
    ]
    browsers = [
        ("No"),
        ("Chrome"),
        ("Unknown"),
        ("Chrome"),
        ("No")
    ]
    devices = [
        ("Android"),
        ("iOS"),
        ("Unknown"),
        ("No"),
        ("iPhone")
    ]

    ListUnion = list(zip(agents, platforms, browsers, devices))

    @pytest.mark.parametrize('agent, platform, browser, device', ListUnion)
    def test_agent_check(self, agent, platform, browser, device):
        response1 = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                 headers={"User-Agent": agent})

        actual_dict_1 = response1.json()
        expected_dict_1 = {
            "user_agent": agent,
            "platform": platform,
            "browser": browser,
            "device": device
        }

        value1_1 = {k: expected_dict_1[k] for k, _ in set(expected_dict_1.items()) - set(actual_dict_1.items())}
        value1_2 = {k: actual_dict_1[k] for k, _ in set(expected_dict_1.items()) - set(actual_dict_1.items())}
        new_list = [value1_1, value1_2]
        print(new_list)
        assert value1_1 == value1_2, f"The difference in data of UserAgent: Expected - {value1_1}, Actual - {value1_2}."

