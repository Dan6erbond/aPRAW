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
    kind: str
        The item's kind / type.
    """

    ID_ATTRIBUTE = "id"

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any] = None, kind: str = ""):
        """
        Initialize the base information.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        """
        self._reddit = reddit
        self._data = data
        self._data_attrs = set()
        self.kind = kind

        if data:
            self._update(data)

    def _update(self, data: Dict[str, Any]):
        """
        Update the base with new information.

        Parameters
        ----------
        data: Dict
            The data obtained from the /about endpoint.
        """
        self._data = data

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                self._data_attrs.add(key)
                setattr(self, key, d[key])
            elif key in self._data_attrs:
                setattr(self, key, d[key])

        if "created_utc" in data:
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

    async def fetch(self):
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: aPRAWBase
            The updated model.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Get a representational string for this model following the pattern ``<{class} {id_attribute}='{id}'>``.

        Returns
        -------
        repr: string
            A printable representational string for this model.
        """
        return f"<{self.__class__.__name__} {self.ID_ATTRIBUTE}='{self._data[self.ID_ATTRIBUTE]}'>"

    @property
    def fullname(self):
        return prepend_kind(self._data[self.ID_ATTRIBUTE], self.kind) if self.kind else self._data[self.ID_ATTRIBUTE]
