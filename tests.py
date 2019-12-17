import asyncio
import re
from datetime import datetime

import apraw
import async_subscan


async def test_subscan(reddit):
    print("Async")
    time_started = datetime.now()
    async for sub in async_subscan.get_eligible():
        if await sub.is_dead():
            print(sub)
    print(datetime.now() - time_started)
    '''
    print("Normal")
    for sub in subscan.get_eligible():
        print(sub)
        '''


async def test_reddit(reddit):
    # print(await reddit.get_request_headers())
    # print(await reddit.message("dan6erbond", "test", "test"))
    # print(await reddit.message("/r/jealousasfuck", "test", "test"))
    print(await reddit.submission("db8k9e"))
    await reddit.submission(
        url="https://www.reddit.com/r/RandomActsOfGaming/comments/db8k9e/uplay_ghost_recon_wildlands")


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
    s = await reddit.submission("db8k9e")
    print(s.title)
    i = 0
    parent_i = 0
    ids = set()
    async for c in s.comments():
        if c.link_id != s.name:
            print(c)
        if c.parent_id == s.name:
            parent_i += 1
        i += 1
        ids.add(c.id)

    print("Comments found:", i)
    print("Unique comments:", len(ids))
    print("Parent-level comments:", parent_i)


async def test_comment(reddit):
    subreddit = await reddit.subreddit("jealousasfuck")
    async for s in subreddit.new(1):
        async for c in s.comments():
            print(await c.author())
            c._submission = None
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

    async for ma in subreddit.mod.log():
        print(ma)

    ids = list()
    async for s in subreddit.stream.submissions():
        if s.id in ids:
            print("Duplicate found:", s.id)
            print(len(ids), " submissions found.")
            break
        ids.append(s.id)
        print(s)
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
