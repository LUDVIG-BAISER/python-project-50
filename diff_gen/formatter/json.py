import json


# Преобразуем объект python в строку json
def format_json(diff):
    return json.dumps(diff)
