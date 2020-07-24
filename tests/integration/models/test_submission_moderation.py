
import pytest

import apraw


class TestSubmissionModeration:
    @pytest.mark.asyncio
    async def test_submission_mod_approve(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.approve()
        await submission.fetch()

        assert submission.approved_by.lower() == reddit.user.username.lower()

    @pytest.mark.asyncio
    async def test_submission_mod_remove(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.remove()
        await submission.fetch()

        assert submission.removed_by.lower() == reddit.user.username.lower()

        await submission.mod.approve()

    @pytest.mark.asyncio
    async def test_submission_mod_lock(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.lock()
        await submission.fetch()

        assert submission.locked

        await submission.mod.unlock()
        await submission.fetch()

        assert not submission.locked

    @pytest.mark.asyncio
    async def test_submission_mod_nsfw(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.mark_nsfw()
        await submission.fetch()

        assert submission.over_18

        await submission.mod.unmark_nsfw()
        await submission.fetch()

        assert not submission.over_18

    @pytest.mark.asyncio
    async def test_submission_mod_spoiler(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.mark_spoiler()
        await submission.fetch()

        assert submission.spoiler

        await submission.mod.unmark_spoiler()
        await submission.fetch()

        assert not submission.spoiler

    @pytest.mark.asyncio
    async def test_submission_mod_flair(self, reddit: apraw.Reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.flair("Test Flair")
        await submission.fetch()

        assert submission.link_flair_text == "Test Flair"
