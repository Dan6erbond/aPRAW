.. currentmodule:: apraw.models

MoreComments
============

This section describes the usage and members of the ``MoreComments`` model.

``MoreComments`` stores a list of IDs pointing to :py:class:`~apraw.models.Comment` and further ``MoreComments``.
These can be retrieved using the :py:func:`~apraw.models.MoreComments.comments` method or by iterating over the instance
asynchronously:

.. code-block:: python3

    comments = await more_comments.comments()
    # or using asynchronous list comprehension:
    comments = [c async for c in more_comments]

.. autoclass:: MoreComments
    :members: