#!/usr/bin/env python

from io import open

from setuptools import setup

"""
:authors: GigantPro
:license: The GPLv3 License (GPLv3)
:copyright: (c) 2024 Xiver organization
"""

with open("pyproject.toml", encoding="utf-8") as file:
    VERSION = file.read().split("=")[2].split('"')[1]

with open("tnotify/README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tnotify",
    version=VERSION,
    author="GigantPro",
    author_email="gigantpro2000@gmail.ru",
    description=("The python lib for telegram notifications"),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/xiver-org/tnotify",
    download_url="https://github.com/xiver-org/tnotify/archive/master.zip",
    license="The GPLv3 License (GPLv3)",
    packages=[
        'tnotify',
        'tnotify.bot_funcs',
        'tnotify.exceptions_driver',
        'tnotify.handlers',
    ],
    install_requires=[
        "aiogram==3.14.0",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
