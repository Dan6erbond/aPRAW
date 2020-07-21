from typing import Any


class BoundedSet:
    """
    A set with a maximum size that evicts the oldest items when necessary.
    This class does not implement the complete set interface.
    """

    def __init__(self, max_items: int):
        """Construct an instance of the BoundedSet."""
        self.max_items = max_items
        self._list = list()
        self._set = set()

    def __contains__(self, item: Any) -> bool:
        """Test if the BoundedSet contains item."""
        return item in self._set

    def add(self, item: Any):
        """Add an item to the set discarding the oldest item if necessary."""
        if len(self._set) == self.max_items:
            self._set.remove(self._list.pop(0))
        self._list.append(item)
        self._set.add(item)
