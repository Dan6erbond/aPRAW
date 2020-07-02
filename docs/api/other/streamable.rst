.. currentmodule:: apraw.models

streamable
==========

``streamable`` is a callable class that can be used as a decorator on functions returning an asynchronous iterator.
It is applied on functions such as :py:func:`~apraw.models.Subreddit.new()` and :py:func:`~apraw.models.Redditor.submissions()`.

Streamable functions can be called by adding ``.stream()``, for example ``reddit.subreddits.new.stream()``.

.. autoclass:: streamable
    :members: