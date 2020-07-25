import pytest

import apraw


class TestModmail:
    @pytest.mark.asyncio
    async def test_modmail(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for conv in subreddit.modmail.conversations():
            assert isinstance(conv, apraw.models.ModmailConversation)

        assert conv

        conversation = await subreddit.modmail(conv.id)
        assert isinstance(conversation, apraw.models.ModmailConversation)

    @pytest.mark.asyncio
    async def test_modmail_conversations(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for conv in subreddit.modmail.conversations():
            assert isinstance(conv, apraw.models.ModmailConversation)

    @pytest.mark.asyncio
    async def test_modmail_messages(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")
        conv = await subreddit.modmail("fqpoa")
        assert conv

        async for msg in conv.messages():
            assert isinstance(msg, apraw.models.ModmailMessage)

    @pytest.mark.asyncio
    async def test_modmail_conversation_reply(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")
        conv = await subreddit.modmail("fqpoa")
        assert conv

        assert await conv.reply("Test response.")

    @pytest.mark.asyncio
    async def test_modmail_conversation_archive(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")
        conv = await subreddit.modmail("eqk7l")
        assert conv

        assert await conv.archive()
        assert await conv.unarchive()

    @pytest.mark.asyncio
    async def test_modmail_conversation_highlight(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")
        conv = await subreddit.modmail("eqk7l")
        assert conv

        assert await conv.highlight()
        assert await conv.remove_highlight()

    @pytest.mark.asyncio
    async def test_modmail_conversation_mute(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")
        conv = await subreddit.modmail("fqpoa")
        assert conv

        try:
            assert await conv.mute()
            assert await conv.unmute()
        except Exception as e:
            assert "CANT_RESTRICT_MODERATOR" in str(e)
