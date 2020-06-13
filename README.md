# aPRAW
Asynchronous Python Reddit API Wrapper by [Dan6erbond](https://dan6erbond.github.io)

**aPRAW** is an asynchronous API wrapper written for the Reddit API that builds on the idea of [PRAW](https://github.com/praw-dev/praw) in many ways. It follows a very similar design, but adds features such as unlimited listings and, most importantly, support for asynchronous requests. This allows the library to be used in scenarios where the requests can take longer (such as with those unlimited listings and streams) and not block other tasks.

## Key Features
 - Asynchronous HTTPS requests to the Reddit API.
 - Unlimited listings.
 - Full OOP class design.
 
## Contributing
aPRAW is an open-source framework which means you can contribute as well! Follow some simple rules so the code stays clean and consistent:
 - Variable and file names must be written in snake-case. (eg. `variable_name`)
 - Class names must be pascal-case. (eg. `ClassName`)
 - Use the OOP approach; create classes when it makes sense.
 - Document as much as you can, preferably with inline comments.
 - Use the reST docstring format.
 - Store data in JSON, INI or YAML format to eliminate dependencies for other formats.
 - Create an `__init__.py` file for sub-modules.
 - Don't use f-strings as they aren't supported in older versions of Python.

## Roadmap
- [ ] Full coverage of Reddit's API.
- [ ] PyPi release.
- [x] Never-ending streams.
- [ ] Useful helper functions.
