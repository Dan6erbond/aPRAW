Quickstart
==========

This section contains a small guide to get started with using aPRAW and its various features.

Those familiar with PRAW will be able to use many features without much additional changes to the code, besides the usage of :code:`async` and :code:`await` syntax.

.. contents::

Creating a Reddit Instance
--------------------------

.. code-block:: python3

    import apraw
    import asyncio


    # instantiate a `Reddit` instance
    # you can also supply a key to an entry within a praw.ini
    # file, making your login compatible with praw as well
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