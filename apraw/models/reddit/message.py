from typing import Dict, Any

from ..helpers.apraw_base import aPRAWBase
from ..mixins.author import AuthorMixin
from ..mixins.subreddit import SubredditMixin
from ...reddit import Reddit


class Message(aPRAWBase, SubredditMixin, AuthorMixin):

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any]):
        super().__init__(reddit, data, reddit.message_kind)