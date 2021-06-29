<<<<<<< HEAD
#print("Hello from Anna Zavyazkina!")

=======
from json.decoder import JSONDecodeError
>>>>>>> develop
import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
<<<<<<< HEAD
=======

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Is not a JSON format, bitch.")

>>>>>>> develop
