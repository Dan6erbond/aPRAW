from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from ...utils import prepend_kind, snake_case_keys

if TYPE_CHECKING:
    from ...reddit import Reddit


class aPRAWBase:
    """
    The base class for Reddit models.

    The ``aPRAWBase`` class stores data retrieved by the endpoints and automatically assigns it as attributes.
    Specific information about the aforementioned attributes can be found in the respective implementations such as :class:`~apraw.models.Comment`.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    kind: str
        The item's kind / type.
    """

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any], kind: str = ""):
        """
        Initialize the base information.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        """
        self.reddit = reddit
        self.kind = kind
        self._update(data)

    def _update(self, data: Dict[str, Any]):
        """
        Update the base with new information.

        Parameters
        ----------
        data: Dict
            The data obtained from the /about endpoint.
        """
        self.data = data

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

        if "created_utc" in data:
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

    @property
    def fullname(self):
        return prepend_kind(self.name if hasattr(
            self, "name") else self.id, self.kind)
