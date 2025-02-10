from pathlib import Path
from gendiff.ya_plakayu import generate_diff
import pytest


# Возвращает полный путь к файлу в папке fixtures
def get_path(file_name: str) -> Path:
    p: Path = Path(__file__)
    current_dir: Path = p.absolute().parent
    return current_dir / 'fixtures' / file_name


test_data: list[tuple[str, str, str, str]] = [
    ('file1.json', 'file2.json', 'stylish', 'result_file1_file2'),
    ('file1.yml', 'file2.yml', 'stylish', 'result_file1_file2'),
    ('file3.json', 'file4.json', 'stylish', 'result_file3_file4'),
    ('file3.yml', 'file4.yml', 'stylish', 'result_file3_file4'),
    ('file3.json', 'file4.json', 'plain', 'result_file3_file4_plain'),
    ('file3.yml', 'file4.yml', 'plain', 'result_file3_file4_plain'),
    ('file3.json', 'file4.json', 'json', 'result_file3_file4_json'),
    ('file3.yml', 'file4.yml', 'json', 'result_file3_file4_json')
]


# Тестирует функцию generate_diff с разными форматами вывода
@pytest.mark.parametrize('file1, file2, format_name, result_file', test_data)
def test_flat_json(file1: str, file2: str, format_name: str, result_file: str) -> None:
    result: str = open(get_path(result_file)).read()
    assert generate_diff(get_path(file1), get_path(file2), format_name) == result
