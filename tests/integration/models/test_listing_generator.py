import pytest


class TestListingGenerator:
    @pytest.mark.asyncio
    async def test_listing_generator_get(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        listing_generator = subreddit.new
        submission_found = False

        async for submission in listing_generator.get():
            if submission.id == "h7mna9":
                submission_found = True
                break

        assert submission_found

    @pytest.mark.asyncio
    async def test_listing_generator_call(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        listing_generator = subreddit.new
        assert listing_generator.__call__ == listing_generator.get

    @pytest.mark.asyncio
    async def test_listing_generator_stream(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        listing_generator = subreddit.new
        submission_found = False

        async for submission in listing_generator.stream():
            if submission.id == "h7mna9":
                submission_found = True
                break

        assert submission_found
