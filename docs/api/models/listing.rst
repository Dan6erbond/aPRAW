.. currentmodule:: apraw.models

Listing
=======

Listings represent arrays returned by the Reddit API. It knows the :py:class:`~apraw.Reddit` instance it's working for,
and contains references to :py:class:`~apraw.models.Subreddit` and :py:class:`~apraw.models.Submission` if available
which are injected to the dynamically parsed aPRAW models.

Raw listings can be fetched with the :py:func:`~apraw.Reddit.get_listing` method where the endpoint needs to be supplied,
and returns a listing.

.. autoclass:: Listing
    :members:
    :special-members: __getitem__, __iter__, __len__, __next__
