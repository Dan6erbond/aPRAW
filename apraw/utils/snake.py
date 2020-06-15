import re
from typing import Any, Dict

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(name: str) -> str:
    return pattern.sub("_", name).lower()


def snake_case_keys(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    return {camel_to_snake(k): v for k, v in dictionary.items()}
