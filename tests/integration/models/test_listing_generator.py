from datetime import datetime

import pytest

import apraw


class TestListingGenerator:
    @pytest.mark.asyncio
    async def test_listing_generator_get(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        listing_generator = subreddit.new

        async for submission in listing_generator.get():
            assert isinstance(submission, apraw.models.Submission)

    @pytest.mark.asyncio
    async def test_listing_generator_call(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        listing_generator = subreddit.new
        assert listing_generator.__call__ == listing_generator.get

    @pytest.mark.asyncio
    async def test_listing_generator_stream(self, reddit):
        subreddit = await reddit.subreddit("askreddit")
        listing_generator = subreddit.new

        i = 0
        async for submission in listing_generator.stream():
            i += 1
            assert isinstance(submission, apraw.models.Submission)
            if i >= 5: break

        time_started = datetime.utcnow()

        i = 0
        async for submission in listing_generator.stream(True):
            i += 1
            assert isinstance(submission, apraw.models.Submission)
            assert submission.created_utc >= time_started
            if i >= 5: break
