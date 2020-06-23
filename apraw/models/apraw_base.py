from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from ..utils import snake_case_keys

if TYPE_CHECKING:
    from ..reddit import Reddit


class aPRAWBase:

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any]):
        self.reddit = reddit
        self._update(data)

    def _update(self, data: Dict[str, Any]):
        self.data = data

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

        if "created_utc" in data:
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])
