from setuptools import setup, find_packages

from cronhelpers.version import __version__

setup(
    name="cronhelpers",
    version=__version__,
    author="Ceshine Lee",
    author_email="ceshine@ceshine.net",
    description="Cron smarter with these small tools.",
    license="MIT License",
    url="",
    packages=['cronhelpers'],
    install_requires=[
        "python-telegram-bot"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    keywords=""
)
