import json
import yaml
from pathlib import Path
from typing import Any, Dict
from gendiff.comparator import create_diff
from gendiff.formatter.stylish import format_style
from gendiff.formatter.plain import format_plain
from gendiff.formatter.json import format_json


# Читаем содержимое файла и возвращаем строку
def get_data_from_file(path: str) -> str:
    with open(path, 'r') as f:
        data = f.read()
    return data


# Преобразуем строку в словарь, в зависимости от формата
def data_to_dict(data: str, ext: str) -> Dict[str, Any]:
    if ext == '.json':
        result = json.loads(data)
    elif ext in ('.yaml', '.yml'):
        result = yaml.load(data, Loader=yaml.FullLoader)
    else:
        raise ValueError('not support format file')  # Ошибка если формат не поддерживается
    return result


# Читаем данные из файла и преобразуем их в словарь
def file_to_dict(path: str) -> Dict[str, Any]:
    data = get_data_from_file(path)
    ext = Path(path).suffix  # Определяем формат файла
    return data_to_dict(data, ext)


# Генерируем разницу между двумя файлами
def generate_diff(file_path1: str, file_path2: str, format_name: str = 'stylish') -> str:
    dict1 = file_to_dict(file_path1)
    dict2 = file_to_dict(file_path2)
    diff = create_diff(dict1, dict2)  # создаем diff между словарями
    return get_formatted_diff(diff, format_name)  # Форматируем результат


# Форматируем diff в заданный формат
def get_formatted_diff(diff: Any, format_name: str = 'stylish') -> str:
    if format_name == 'stylish':
        return format_style(diff)
    elif format_name == 'plain':
        return format_plain(diff)
    elif format_name == 'json':
        return format_json(diff)
    else:
        raise ValueError('not support formatted name')  # Ошибка если формат неизвестен
