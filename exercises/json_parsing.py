import json

string_as_json_format = '{"answer": "Hello, User"}'
obj = json.loads(string_as_json_format)
#print(obj['answer'])

key = "answer2"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} тут неть >.< ")


