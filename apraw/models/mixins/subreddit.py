from ..subreddit.subreddit import Subreddit


class SubredditMixin:
    """
    Mixin for items in a subreddit.
    """

    def __init__(self, subreddit: Subreddit = None):
        self._subreddit = subreddit

    async def subreddit(self) -> Subreddit:
        """
        Retrieve the subreddit this item was made in as a :class:`~apraw.models.Subreddit`.

        Returns
        -------
        subreddit: Subreddit
            The subreddit this item was made in.
        """
        if self._subreddit is None:
            self._subreddit = await self._reddit.subreddit(self._data["subreddit"])
        return self._subreddit
