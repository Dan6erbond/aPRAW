from typing import Dict, Any, TYPE_CHECKING

from ..helpers.apraw_base import aPRAWBase
from ..mixins.author import AuthorMixin
from ..mixins.replyable import ReplyableMixin
from ..mixins.subreddit import SubredditMixin

if TYPE_CHECKING:
    from ...reddit import Reddit


class Message(aPRAWBase, SubredditMixin, AuthorMixin, ReplyableMixin):
    """
    The model representing comments.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    =========================== ======================================================================================
    Attribute                   Description
    =========================== ======================================================================================
    ``first_message``           The first message sent in the message thread if the current message wasn't the first.
    ``first_message_name``      The fullname of the first message in the message thread if applicable.
    ``subreddit``               The subreddit this conversation is being held in if applicable.
    ``likes``                   ``None``
    ``replies``                 A list of all the message replies if applicable, otherwise an empty string.
    ``id``                      The message ID.
    ``subject``                 The subject of this message's thread.
    ``associated_awarding_id``  The ID of the associated awarding if the message was sent in the context of an award.
    ``score``                   ``0``
    ``author``                  The username of the message's author.
    ``num_comments``            The number of comments in this message's thread.
    ``parent_id``               ``None``
    ``subreddit_name_prefixed`` The prefixed name of the subreddit this conversation is being held in if applicable.
    ``new``                     ``bool``
    ``type``                    ``str``
    ``body``                    The markdown string contents of this message.
    ``dest``                    The recipient of the message.
    ``body_html``               The HTML string contents of this message.
    ``was_comment``             Whether this message was a comment.
    ``name``                    The fullname of this message, representing the ID prefixed with its kind. (e.g. `t4_`)
    ``created``                 The timestamp on which this message was created.
    ``created_utc``             The parsed UTC ``datetime`` on which this message was created.
    ``context``                 ``str``
    ``distinguished``           The type of distinguishment on this message object.
    =========================== ======================================================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any]):
        """
        Create an instance of a Message object.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data, reddit.message_kind)
        AuthorMixin.__init__(self)
        SubredditMixin.__init__(self)
