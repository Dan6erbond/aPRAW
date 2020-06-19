import pytest


class TestModmail:
    @pytest.mark.asyncio
    async def test_modmail_conversations(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        modmail = subreddit.modmail
        conversation = None

        async for conv in modmail.conversations():
            if conv.subject == "invitation to moderate /r/aPRAWTest":
                conversation = conv
                break

        assert conversation != None
        assert conversation.id == "er3yc"
