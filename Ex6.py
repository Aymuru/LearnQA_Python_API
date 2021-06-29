import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
list_history = response.history
count = len(list_history)

for i in list_history:
    print(i.url)

print(f"Number of redirects = {count}.")
print(f"Final page - {response.url}.")