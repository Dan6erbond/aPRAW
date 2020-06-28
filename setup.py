import setuptools
from apraw import __version__, __tag__

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aPRAW",
    version="{}-{}".format(__version__, __tag__) if __tag__ else __version__,
    author="Dan6erbond",
    author_email="moravrav@gmail.com",
    description="aPRAW is an asynchronous Reddit API wrapper written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dan6erbond/aPRAW",
    packages=setuptools.find_packages(include=['apraw', 'apraw.*']),
    install_requires=[
        'aiohttp>=3.6.2'
    ],
    keywords="reddit api wrapper async",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    license="GNU General Public License v3 (GPLv3)",
    python_requires='>=3.6',
)

# classifiers can be found here: https://pypi.org/classifiers/
