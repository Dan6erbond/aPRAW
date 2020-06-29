.. currentmodule:: apraw.models

Submission
==========

A Submission can either be instantiated by using its ID, or by going through subreddits:

.. code-block:: python3

    submission = await reddit.submission("h7mna9")

    sub = await reddit.redditor("aprawbot")
    async for submission in sub.new():
        print(submission)

.. autoclass:: Submission
    :members:
    :inherited-members:
