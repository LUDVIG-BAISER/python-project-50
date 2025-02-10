# Преобразуем входное значение в строку.
def to_string(x):
    if x is None:
        result = 'null'
    elif isinstance(x, bool):
        result = 'false'
        if x:
            result = 'true'
    else:
        result = str(x)
    return result
