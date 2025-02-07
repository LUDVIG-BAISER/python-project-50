from diff_gen.formatter.common import to_string

from typing import Any, Dict, List

ONE_INDENT: str = '    '  # Отступ в 4 пробела


# Форматируем отступы к diff
def format_style(diff: List[Dict[str, Any]], level: int = 1) -> str:
    lines: List[str] = []
    for item in diff:
        lines.extend(get_list_lines(item, level))  # Получаем строки для каждого элемента
    lines.insert(0, '{')
    lines.append(get_indent(level - 1) + '}')
    return '\n'.join(lines)


# Форматируем строки для элементов diff
def get_list_lines(item: Dict[str, Any], level: int) -> List[str]:
    lines: List[str] = []
    status: str = item['status']
    key: str = item['key']
    new_value: Any = item.get('new_value')
    old_value: Any = item.get('old_value')
    indent: str = get_indent(level)  # отступ для текущего уровня

    if status == 'nested':  # Обрабатываем вложенные структуры
        nested_diff = item['nested']
        lines.append(f"{indent}{key}: {format_style(nested_diff, level + 1)}")
    elif status == 'equal':  # Значение не изменилось
        lines.append(f"{indent}{key}: {get_value(old_value, level)}")
    elif status == 'deleted':  # Удаленное значение
        lines.append(f"{indent[:-2]}- {key}: {get_value(old_value, level)}")
    elif status == 'added':  # Добавленное значение
        lines.append(f"{indent[:-2]}+ {key}: {get_value(new_value, level)}")
    elif status == 'changed':  # Измененное значение
        lines.append(f"{indent[:-2]}- {key}: {get_value(old_value, level)}")
        lines.append(f"{indent[:-2]}+ {key}: {get_value(new_value, level)}")
    else:
        raise ValueError("error in format diff")  # Ошибка если статус неизвестен
    return lines


# Преобразуем значение в строку с учетом типа
def get_value(value: Any, level: int) -> str:
    if isinstance(value, dict):
        return dict_to_str(value, level)  # Обрабатываем вложенный словарь
    return to_string(value)  # Для остальных типов используется to_string


# Преобразуем словарь в строку с форматированием
def dict_to_str(dict_: Dict[str, Any], level: int) -> str:
    lines: List[str] = ['{']
    for key in sorted(dict_.keys()):
        value: Any = dict_[key]
        if isinstance(value, dict):
            formatted_value = dict_to_str(value, level + 1)
        else:
            formatted_value = to_string(value)
        lines.append(f"{get_indent(level + 1)}{key}: {formatted_value}")
    lines.append(get_indent(level) + '}')
    return '\n'.join(lines)


# Генерируем отступ на основе уровня вложенности.
def get_indent(level: int) -> str:
    return ONE_INDENT * level
