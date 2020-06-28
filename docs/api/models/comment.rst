.. currentmodule:: apraw.models

Comment
=======

Besides retrieving comments similarly to submissions using their ID or fetching them through a subreddit's listings,
comments can be obtained from the submission they were made in like so:

.. code-block:: python3

    submission = await reddit.submission("h7mna9")

    async for comment in submission.comments():
        print(comment)

.. autoclass:: Comment
    :members: