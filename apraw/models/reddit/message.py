from typing import Dict, Any, TYPE_CHECKING

from ..helpers.apraw_base import aPRAWBase
from ..mixins.author import AuthorMixin
from ..mixins.replyable import ReplyableMixin
from ..mixins.subreddit import SubredditMixin

if TYPE_CHECKING:
    from ...reddit import Reddit


class Message(aPRAWBase, SubredditMixin, AuthorMixin, ReplyableMixin):

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any]):
        super().__init__(reddit, data, reddit.message_kind)
