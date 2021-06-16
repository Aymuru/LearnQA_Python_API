#print("Hello from Anna Zavyazkina!")

import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
