import requests

# Задание1
response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Задание 1: ", response1, response1.text, "---- Ответ 200, но метод неверный")
print("")

# Задание2
response2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Задание 2: ", response2, response2.text, "---- Ответ 400, потому что метода не из разрешенного списка")
print("")

# Задание3
payload = {"method": "PUT"}
response3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
print("Задание 3: ", response3, response3.text, "---- Ответ 200, при использовании параметра возвращается success")
print("")

# Задание4
print("Задание 4: ")
param_list = ["GET", "POST", "PUT", "DELETE"]
for i in param_list:
    resp1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": i})
    print(resp1.status_code, resp1.text, "GET - ожидаемый метод,", i)
    resp2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print(resp2.status_code, resp2.text, "POST - ожидаемый метод,", i)
    resp3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print(resp3.status_code, resp3.text, "PUT - ожидаемый метод,", i)
    resp4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    print(resp4.status_code, resp4.text, "DELETE - ожидаемый метод,", i)
    print("------------")

print("---- Метод GET с параметром method:DELETE возвращает success, хотя не должен.")

