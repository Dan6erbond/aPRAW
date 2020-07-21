.. currentmodule:: apraw.models

Subreddit Moderation
====================

This section details the usage of models related to subreddit moderation.

.. contents::

SubredditModerator
------------------

Subreddit moderators are usually retrieved as follows:

.. code-block:: python3

    sub = await reddit.subreddit("aprawtest")
    moderators = []
    async for moderator in sub.moderators():
        moderators.append(str(moderator))

.. autoclass:: apraw.models.SubredditModerator
    :members:

SubredditModeration
-------------------

Items in the modqueue can be fetched using the ``modqueue`` listing:

.. code-block:: python3

    sub = await reddit.subreddit("aprawtest")
    async for item in sub.mod.modqueue(): # can also be streamed
        print(type(item))
        >>> apraw.models.Comment or apraw.models.Submission

.. autoclass:: apraw.models.SubredditModeration
    :members:

SubredditSettings
-----------------

.. autoclass:: apraw.models.SubredditSettings
    :members:
    :inherited-members:

ModAction
---------

.. autoclass:: apraw.models.ModAction
    :members:
