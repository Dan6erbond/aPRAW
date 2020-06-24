.. currentmodule:: apraw.models

Subreddit Moderation
====================

This section details the usage of models related to subreddit moderation.

.. contents::

SubredditModerator
__________________

Subreddit moderators are usually retrieved as follows:

.. code-block:: python3

    sub = await reddit.subreddit("aprawtest")
    moderators = []
    async for moderator in sub.moderators():
        moderators.append(str(moderator))

.. autoclass:: apraw.models.subreddit.SubredditModerator
    :members: