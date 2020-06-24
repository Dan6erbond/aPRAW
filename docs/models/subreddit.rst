.. currentmodule:: apraw.models

Subreddit
=========

This section describes the API of the Subreddit model and its helpers.

.. contents::

Subreddit
_________

A subreddit can be instantiated as follows:

.. code-block:: python3

    sub = await reddit.subreddit("aprawtest")

.. autoclass:: Subreddit
    :members:

SubredditModerator
__________________

Subreddit moderators are usually retrieved as follows:

.. code-block::python3

    sub = await reddit.subreddit("aprawtest")
    moderators = []

    async for moderator in subreddit.moderators():
        moderators.append(moderator)

.. autoclass:: apraw.models.subreddit.SubredditModerator
    :members: