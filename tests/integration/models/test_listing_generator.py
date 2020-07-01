from datetime import datetime

import pytest

import apraw


class TestListingGenerator:
    @pytest.mark.asyncio
    async def test_listing_generator_get(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        submission_found = False

        async for submission in subreddit.new():
            if submission.id == "h7mna9":
                submission_found = True
                break

        assert submission_found

    @pytest.mark.asyncio
    async def test_listing_generator_stream(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        submission_found = False

        async for submission in subreddit.new.stream():
            if submission.id == "h7mna9":
                submission_found = True
                break

        assert submission_found
