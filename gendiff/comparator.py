from typing import Any, Dict, List


# Создаем список различий между двумя словарями
def create_diff(tree1: Dict[str, Any],
                tree2: Dict[str, Any]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    tree1_keys = tree1.keys()
    tree2_keys = tree2.keys()
    all_keys = sorted(set(tree1_keys) | set(tree2_keys))  # Все уникальные ключи
    added_keys = tree2_keys - tree1_keys  # Ключи первого словаря
    deleted_keys = tree1_keys - tree2_keys  # Ключи второго словаря
    for key in all_keys:
        item: Dict[str, Any] = {"key": key}
        value1 = tree1.get(key)
        value2 = tree2.get(key)
        if key in added_keys:  # Ключ был добавлен
            item["status"] = "added"
            item["new_value"] = value2
        elif key in deleted_keys:  # Ключ был удален
            item["status"] = "deleted"
            item["old_value"] = value1
        elif isinstance(value1, dict) and isinstance(
                value2, dict
        ):  # Оба значения словари
            item["status"] = "nested"
            item["nested"] = create_diff(
                value1, value2
            )  # рекурсия для вложенных структур
        elif value1 == value2:  # Значения равны
            item["status"] = "equal"
            item["old_value"] = value1
        else:  # Значения изменились
            item["status"] = "changed"
            item["old_value"] = value1
            item["new_value"] = value2

        result.append(item)  # Добавляем результат в список
    return result  # Возвращаем список различий.
