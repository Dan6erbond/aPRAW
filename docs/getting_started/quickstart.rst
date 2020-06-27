Quickstart
==========

This section contains a small guide to get started with using aPRAW and its various features.

.. contents::

Creating a Reddit Instance
--------------------------

Currently aPRAW only supports the use of a script auth flow to log in to Reddit and perform requests. Read-only modes as well as the application flow are WIP.

To obtain a ``client_id`` and ``client_secret`` for your application, head to Reddit's `App Preferences <https://www.reddit.com/prefs/apps>`_ and create a new app.
Follow the guidelines on `Reddit's Quick Start Example <https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example>`_ to obtain your credentials.

Those credentials can now be used to create a Reddit instance:

.. code-block:: python3

    import apraw


    # instantiate a `Reddit` instance
    # you can also supply a key to an entry within a praw.ini
    # file, making your login compatible with praw as well
    reddit = apraw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET",
                        password="PASSWORD", user_agent="USERAGENT",
                        username="USERNAME")

Those previously making use of a ``praw.ini`` file can continue to do so, by specifying the key that was used for the client in place of the credentials.
aPRAW will then automatically search for the file and save those credentials.

For more information on ``praw.ini`` files visit `PRAW's documentation <https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html>`_.

Running Asynchronous Code
-------------------------

Since most of aPRAW's code are asynchronous functions or generators, you will want to add your tasks to an event loop such as the ``asyncio`` one.

For that do the following:

.. code-block:: python3

    import apraw
    import asyncio

    # instantiate a `Reddit` instance
    reddit = apraw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET",
                        password="PASSWORD", user_agent="USERAGENT",
                        username="USERNAME")

    async def scan_posts():
      # get an instance of a subreddit
      subreddit = await reddit.subreddit("aprawtest")

      # loop through new posts
      async for submission in subreddit.new():
        print(submission.title)

    if __name__ == "__main__":
        # get the asyncio event loop
        loop = asyncio.get_event_loop()

        # add scan_posts() to the queue and run it
        loop.run_until_complete(scan_posts())

Basic Concepts
--------------

aPRAW assumes that all the Reddit items know the logged-in Reddit instance.
When grabbing items by using the built-in functions, this will be done automatically through dependency injection.

Instantiating items with the API is very easy:

.. code-block:: python3

    # instantiate a `Reddit` instance
    reddit = apraw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET",
                        password="PASSWORD", user_agent="USERAGENT",
                        username="USERNAME")

    # grab an instance of the /r/aPRAWTest subreddit
    subreddit = await reddit.subreddit("aprawtest")

    # grab an instance of the /u/aPRAWBot Redditor
    redditor = await reddit.redditor("aprawbot")

    # grab a test submission made on /r/aPRAWTest
    submission = await reddit.submission("h7mna9")

    # grab a test comment made on /r/aPRAWTest
    comment = await reddit.comment("fulsybg")

Looping Through Items
*********************

Most endpoints returning list or "`listings`" of items are represented by async generators in aPRAW. To grab a set of new posts on a subreddit try this:

.. code-block:: python3

    # get an instance of a subreddit
    subreddit = await reddit.subreddit("aprawtest")

    # loop through new posts
    async for submission in subreddit.new():
        print(submission.id)

In cases where :py:class:`~apraw.models.ListingGenerator` is used, ``**kwargs`` can be passed into the endpoint as well.

Streaming Items
***************

:py:class:`~apraw.models.ListingGenerator` has a built-in :py:func:`~apraw.models.ListingGenerator.stream` method that will poll the Reddit API endpoint it's mapped to, and yield items as they come.
This is done in a very efficient manner with an internal tracker for items, an exponential function to increase wait times and the use of ``asyncio.sleep()`` to ensure non-blocking streams.

Polling an endpoint with :py:class:`~apraw.models.ListingGenerator` is as simple as writing:

.. code-block:: python3

    # get an instance of a subreddit
    subreddit = await reddit.subreddit("aprawtest")

    # stream new posts
    async for submission in subreddit.new.stream():
        print(submission.id)