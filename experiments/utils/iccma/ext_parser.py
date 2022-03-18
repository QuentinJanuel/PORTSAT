from typing import List


def parse_extension(ext: str) -> List[str] | None:
    if ext.strip() == "NO":
        return None
    return _parse_list(ext)  # type: ignore


def parse_extensions(ext: str) -> List[List[str]]:
    return _parse_list(ext)  # type: ignore


def _parse_list(string: str):
    if string[0] != "[":
        return string
    inner = string.strip()[1:-1]
    if len(inner) == 0:
        return []
    values = []
    current_val = ""
    nested_level = 0
    for char in inner:
        if char == "[":
            nested_level += 1
        elif char == "]":
            nested_level -= 1
        if char == "," and nested_level == 0:
            values.append(current_val)
            current_val = ""
        else:
            current_val += char
    values.append(current_val)
    return [_parse_list(val) for val in values]
