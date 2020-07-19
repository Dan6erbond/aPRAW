.. currentmodule:: apraw.models

ListingGenerator
================

``ListingGenerator`` is a utility class that fetches items from the listing endpoint, parses the response, and yields items as they are found.
If the item kind cannot be identified, :py:class:`~apraw.models.aPRAWBase` is returned which automatically assigns itself all the data attributes found.

.. autoclass:: ListingGenerator
    :members: