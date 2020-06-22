import pytest

import apraw


class TestSubredditWiki:

    @pytest.mark.asyncio
    async def test_subreddit_wiki(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        assert "index" in await subreddit.wiki()

    @pytest.mark.asyncio
    async def test_subreddit_wiki_page(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        wiki_page = await subreddit.wiki.page("index")

        assert "# Test Wiki Page" in wiki_page.content_md
        assert "### Some more text." in wiki_page.content_md

        LOREM_IPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
        exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
        sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
        est laborum."""

        assert " ".join(
            [line.strip() for line in LOREM_IPSUM.split("\n")]) in wiki_page.content_md

    @pytest.mark.asyncio
    async def test_subreddit_wiki_revisions(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for revision in subreddit.wiki.revisions():
            assert hasattr(revision, "page")
            assert isinstance(revision, apraw.models.WikipageRevision)
            assert isinstance(revision.author, apraw.models.Redditor)
