from gendiff.formatter.common import to_string

from typing import Any, Dict, List, Optional


# Форматируем разницу (diff) в виде plain-текста
def format_plain(diff: List[Dict[str, Any]], path: str = "") -> str:
    lines: List[str] = []
    for item in diff:
        current_path: str = f"{path}.{item['key']}" if path else item["key"]
        line: Optional[str] = make_line(item, current_path)
        if line is not None:
            lines.append(line)
    return "\n".join(lines)


# Создаем строку для конкретного элемента diff
def make_line(item: Dict[str, Any], path: str) -> Optional[str]:
    status: str = item["status"]
    if status == "equal":
        return None
    if status == "nested":
        return format_plain(item["nested"], path)

    actions = {
        "added": lambda: f"added with value: {get_value(item['new_value'])}",
        "deleted": lambda: "removed",
        "changed": lambda: f"updated. From {get_value(item['old_value'])} to"
                           f" {get_value(item['new_value'])}",
    }

    if status in actions:
        return f"Property '{path}' was {actions[status]()}"

    raise ValueError("error in format diff")


# Преобразуем значение в строку в зависимости от типа
def get_value(value: Any) -> str:
    if isinstance(value, dict):
        return "[complex value]"
    if isinstance(value, str):
        return f"'{value}'"
    return to_string(value)
