import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aPRAW",
    version="0.2.0-alpha",
    author="Dan6erbond",
    author_email="moravrav@gmail.com",
    description="Asynchronous Python Reddit API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dan6erbond/aPRAW",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed"
    ],
    python_requires='>=3.6',
)

# classifiers can be found here: https://pypi.org/classifiers/
