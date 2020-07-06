
import pytest

import apraw


class TestSubmissionModeration:
    @pytest.mark.asyncio
    async def test_submission_mod_approve(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.approve()
        submission = await reddit.submission("h7mna9")

        assert submission.approved_by.lower() == reddit.user.username.lower()

    @pytest.mark.asyncio
    async def test_submission_mod_remove(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.remove()
        submission = await reddit.submission("h7mna9")

        assert submission.removed_by.lower() == reddit.user.username.lower()

        await submission.mod.approve()

    @pytest.mark.asyncio
    async def test_submission_mod_lock(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.lock()
        submission = await reddit.submission("h7mna9")

        assert submission.locked

        await submission.mod.unlock()
        submission = await reddit.submission("h7mna9")

        assert not submission.locked

    @pytest.mark.asyncio
    async def test_submission_mod_nsfw(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.mark_nsfw()
        submission = await reddit.submission("h7mna9")

        assert submission.over_18

        await submission.mod.unmark_nsfw()
        submission = await reddit.submission("h7mna9")

        assert not submission.over_18

    @pytest.mark.asyncio
    async def test_submission_mod_spoiler(self, reddit):
        submission = await reddit.submission("h7mna9")
        await submission.mod.spoiler()
        submission = await reddit.submission("h7mna9")

        assert submission._data["spoiler"]

        await submission.mod.unspoiler()
        submission = await reddit.submission("h7mna9")

        assert not submission._data["spoiler"]
