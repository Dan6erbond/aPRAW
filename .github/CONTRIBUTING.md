# Contributing to aPRAW

If you're reading this, first of all, thank you for considering to contribute to the aPRAW project! It makes the library substantially better and much more pleasant to use for developers in the future.

**Table of Contents**
 - [Questions](#i-dont-want-to-read-all-this-i-just-have-a-question)
 - [Reporting Bugs](#reporting-bugs)
 - [Pull Requests](#submitting-pull-requests)
   - [Tests](#tests)
   - [Commit Guidelines](#git-commit-guidelines)
   - [Code Guidelines](#code-guidelines)

## I don't want to read all this! I just have a question!

> Please don't use issues to ask questions. Instead use one of the many other resources listed below to get in contact with the developers!

 - Join the [/r/aPRAW](https://reddit.com/r/aPRAW) subreddit
   - Feel free to post a question in the questions thread or make your own post if it could start a big discussion!
 - Join the [aPRAW Discord server](https://discord.gg/66avTS7)
   - Use `#💬general-chat` for discussion about the library and talking to other users.
   - Use `#❓questions` to post questions. The developers will try to get back to you as quickly as possible, but other users can help as well!
   - Use `#💡ideas` if you have any ideas for the framework but don't know how to implement them, or just want to throw in the suggestion.
   - If you're a contributor you also get a fancy role and any discussion about contributing can be held in `#💬coder-chat`.

## Reporting Bugs

Please be aware of a couple of things when filing bug reports:

1. Don't report duplicate bugs. Check previously filed reports to make sure it's unique.
2. If you have a traceback of your bug, make sure to include it in the issue. It makes it much easier for the developers to find out what went wrong.
3. Provide enough information about what happened. Include at least the following:
    - A summary that describes the issue.
    - How to reproduce the issue, include the code that was used. Make sure to remove any sensitive information.
    - Tell us what you expected to happen, and what happened instead.
    - Add some information about the environment. Knowing your operating system, Python version and packages installed is valuable in finding out what went wrong.

## Submitting Pull Requests

If you're here and have some additions to make to the code, awesome! Submitting a pull request is pretty simple, just follow some guidelines and try to keep everything consistent. This project follows most of the PEP-8 guidelines.

Make sure your pull requests focus on single issues or features, so that tests can be performed quickly. Tests will be ran automatically through GitHub CI Actions. A Linter (`flake8`) will also be ran during this process.

### Tests

Write test cases with the PyTest framework and use the `reddit` fixture if you need access to an authenticated client like so:

```python
# can be async due to the usage of the `pytest-asyncio` fixture library
# `reddit` argument is being fed dynamically by a fixture in `conftest.py`
async def test_case(self, reddit):
    subreddit = await self._reddit.subreddit("aPRAWTest")
    assert subreddit.description == "Testing subreddit for aPRAW."
```

### Git Commit Guidelines

 - When making additions to the code, make sure you [link issues to your pull request](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue).
 - Use the present tense. (e.g. "Add feature", not "Added feature")

### Code Guidelines

 - Limit lines to 119 characters or less.
 - Variable and file names must be written in snake-case. (e.g. `variable_name`)
 - Class names must be pascal-case. (e.g. `ClassName`)
 - Use the OOP approach; create classes when it makes sense.
 - Document as much as you can, preferably with inline comments.
 - Use the NumPy docstring format.
 - Store data in JSON, INI or YAML format to eliminate dependencies for other formats.
 - Create an `__init__.py` file for sub-modules.
 - Don't use f-strings as they aren't supported in older versions of Python.
