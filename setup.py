from setuptools import setup, find_packages
from distutils.util import convert_path
from typing import Any, Dict

# https://stackoverflow.com/a/24517154/4575168
main_ns: Dict[str, Any] = {}
ver_path = convert_path('cronhelpers/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="cronhelpers",
    version=main_ns['__version__'],
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
