import asyncio
import re

import apraw
import async_subscan
import subscan


async def test_subscan(reddit):
    print("Async")
    async for sub in async_subscan.get_eligible():
        print(sub)
    print("Normal")
    for sub in subscan.get_eligible():
        print(sub)


async def test_reddit(reddit):
    print(await reddit.get_request_headers())
    print(await reddit.message("dan6erbond", "test", "test"))
    print(await reddit.message("/r/jealousasfuck", "test", "test"))


async def test_redditor(reddit):
    redditor = await reddit.redditor("dan6erbond")
    # print(await redditor.message("test", "test"))
    # async for sub in redditor.moderated_subreddits():
        # print(sub)
    async for c in redditor.comments():
        s = await c.submission()
        print(await s.subreddit())

    async for s in redditor.submissions():
        print(await s.subreddit())


async def test_submission(reddit):
    subreddit = await reddit.subreddit("jealousasfuck")
    async for s in subreddit.new(1):
        print(await s.author())
        print(await s.subreddit())


async def test_comment(reddit):
    subreddit = await reddit.subreddit("jealousasfuck")
    async for s in subreddit.new(1):
        async for c in s.comments():
            print(await c.author())
            sub = await c.submission()
            print(sub.id == s.id)
            break


async def test_subreddit(reddit):
    # subreddit = await reddit.subreddit("test")
    # print(await subreddit.message("test", "test"))
    subreddit = await reddit.subreddit("jealousasfuck")
    ids = list()
    duplicates = False
    async for s in subreddit.new(None):
        if s.id in ids:
            duplicates = True
            break
        ids.append(s.id)
    if len(ids) > 0 and not duplicates:
        print("Test passed.")
    else:
        print("Test failed.")
    # async for mod in subreddit.moderators():
    # print(dir(await mod.redditor()))


async def test_subreddit_moderation(reddit):
    subreddit = await reddit.subreddit("jealousasfuck")
    async for i in subreddit.mod.reports():
        print(i.user_reports)
        print(i.mod_reports)


async def test_subreddits(reddit):
    ids = list()
    async for s in reddit.subreddits.new(limit=200):
        ids.append(s.id)
        print("{}:".format(len(ids)), s, "Subscribers:", s.subscribers)


async def test_modmail(reddit):
    subreddit = await reddit.subreddit("jealousasfuck")
    async for c in subreddit.modmail.conversations():
        async for m in c.messages():
            print(m.body_md)
            break
        break


tests = [test_subscan, test_reddit, test_redditor, test_subreddit, test_subreddit_moderation, test_subreddits,
         test_redditor, test_submission, test_comment, test_modmail]


async def run_tests():
    reddit = apraw.Reddit("D6B")
    i = 0
    for test in tests:
        print("{}:".format(i), test)
        i += 1
    while True:
        i = input("Select a test to run: ")
        try:
            i = int(i)
            if i >= 0 and i < len(tests):
                await tests[i](reddit)
            else:
                print("No test found at position {}!".format(i))
        except Exception as e:
            s = re.search("^(\d+)$", i)
            if s is None:
                break


loop = asyncio.get_event_loop()
loop.run_until_complete(run_tests())
