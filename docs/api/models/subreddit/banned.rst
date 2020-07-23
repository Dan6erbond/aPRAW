.. currentmodule:: apraw.models

Subreddit Banned
================

This section details the usage of models related to banned users of a subreddit.

.. contents::

SubredditBanned
---------------

A helper class to aid in interacting with a subreddit's banned users.

.. autoclass:: apraw.models.SubredditBanned
    :members:

BannedUser
----------

Banned users can be fetched doing the following:

.. code-block:: python3

    sub = await reddit.subreddit("aprawtest")
    async for item in sub.banned(): # can also be streamed
        print(type(item))
        >>> apraw.models.BannedUser

.. autoclass:: apraw.models.BannedUser
    :members:
    :inherited-members: redditor, fullname
    :special-members: __str__
