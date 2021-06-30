import json

import requests
import time

#method = {"token": "GET"}

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print("Запрос GET без передачи метода token: ", response1.text)

token_take = response1.json()['token']
time_take = response1.json()['seconds']
print("Извлекли токен: ", token_take, "----- Время выполнения: ", time_take)

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token_take})
print("Сделали запрос с token ДО того как задача готова: ", response2.json())

assert response2.json()['status'] == "Job is NOT ready", "Статус неверный"

print("Подождем время выполнения...")
time.sleep(time_take)

response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token_take})
print("Сделали запрос с token ПОСЛЕ того как задача готова: ", response3.json())

assert response3.json()['status'] == "Job is ready", "Статус неверный"
assert response3.json()['result'] != None, "Результата нет"

