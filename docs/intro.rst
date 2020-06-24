Introduction
============

This is the documentation for aPRAW, a wrapper library for Python to aid in performing asynchronous requests to the Reddit API and interacting with its data.

Prerequisites
-------------

aPRAW works with Python 3.6 or higher.

Installing
----------

aPRAW can be installed directly from PyPi:

.. code-block:: shell

    $ pip install aPRAW

Basic Concepts
--------------

aPRAW assumes that all the Reddit items know the logged-in Reddit instance. When grabbing items by using the built-in functions, this will be done automatically.

Instantiating items with the API is very easy:

.. code-block:: python3

    reddit = apraw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                    password=PASSWORD, user_agent=USER_AGENT,
                    username=USERNAME)

    subreddit = await reddit.subreddit("aprawtest")
    redditor = await reddit.redditor("aprawbot")
    submission = await reddit.submission("h7mna9")
    comment = await reddit.comment("fulsybg")