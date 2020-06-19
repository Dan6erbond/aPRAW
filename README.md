# aPRAW

Asynchronous Python Reddit API Wrapper by [Dan6erbond](https://dan6erbond.github.io)

**aPRAW** is an asynchronous API wrapper written for the Reddit API that builds on the idea of [PRAW](https://github.com/praw-dev/praw) in many ways. It follows a very similar design, but adds features such as unlimited listings and, most importantly, support for asynchronous requests. This allows the library to be used in scenarios where the requests can take longer (such as with those unlimited listings and streams) and not block other tasks.

**Table of Contents**
 - [Key Features](#key-features)
 - [Reporting Bugs](#installation)
 - [Pull Requests](#quickstart)
 - [Community and Support](#community-and-support)
   - [Contributing](#contributing)
 - [Documentation](#documentation)
 - [Roadmap](#roadmap)
 - [License](#license)

## Key Features

 - Asynchronous HTTPS requests to the Reddit API.
 - Unlimited listings.
 - Full OOP class design.

## Installation

aPRAW requires a release of Python 3.6 or newer as it uses the inbuilt `async` and `await` syntax. You can install aPRAW via pip:

```pip install apraw```

## Quickstart

Create an application on your Reddit account as per their [documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example). Once you have that, you can interact with aPRAW and its subclasses:

```python
import apraw
import asyncio


# instantiate a `Reddit` instance
# you can also supply a key to an entry within a praw.ini
# file, making your login compatible with praw as well
reddit = apraw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET",
                    password="PASSWORD", user_agent="USERAGENT",
                    username="USERNAME")

async def scan_posts():
  # get an instance of a subreddit
  subreddit = await reddit.subreddit("aprawtest")

  # loop through new posts
  async for submission in subreddit.new():
    print(submission.title)

if __name__ == "__main__":
    # get the asyncio event loop
    loop = asyncio.get_event_loop()

    # add scan_posts() to the queue and run it
    loop.run_until_complete(scan_posts())
```

Due to the fact that aPRAW's code is almost entirely asynchronous, you will have to perform all network-related tasks within the asyncio event loop.

## Community and Support

If you have any questions regarding aPRAW and its usage...

 - Join the [/r/aPRAW](https://reddit.com/r/aPRAW) subreddit
   - Feel free to post a question in the questions thread or make your own post if it could start a big discussion!
 - Join the [aPRAW Discord server](https://discord.gg/66avTS7)
   - Use the `#💬general` chat for discussion about the library and talking to other users.
   - Use the `#❓questions` to post questions. The developers will try to get back to you as quickly as possible, but other users can help as well!
   - Use the `#💡ideas` if you have any ideas for the framework but don't know how to implement them, or just want to throw in the suggestion.
   
### Contributing
   
Of course, aPRAW is open-source under the GPLv3 license and all additions and bug reports in the form of issues and pull requests are welcome! For further information, view the [contribution guidelines](.github/CONTRIBUTING.md) and have fun coding!

## Documentation

Still on its way!

## Roadmap

- [ ] Full coverage of Reddit's API.
- [x] PyPi release.
- [x] Never-ending streams.
- [ ] Useful helper functions.

## License
PRAW's source is provided under GPLv3.
> Copyright ©, RaviAnand Mohabir
