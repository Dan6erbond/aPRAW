from datetime import datetime
from typing import Any, Dict

from ..utils import snake_case_keys


class aPRAWBase:
    def __init__(self, reddit, data: Dict[str, Any]):
        self.reddit = reddit
        self.data = data

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

        if "created_utc" in data:
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])
