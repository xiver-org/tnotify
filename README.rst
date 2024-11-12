.. raw:: html

   <p align="center">
        <h1 align="center">Tnotify</h1>
        <h2 align="center"> The python lib for fast telegram notifications.</h2>
    </p>

    <p align="center">
        <a href="https://pypi.python.org/pypi/tnotify"><img alt="Pypi version" src="https://img.shields.io/pypi/v/tnotify.svg"></a>
        <a href="https://pypi.python.org/pypi/tnotify"><img alt="Python versions" src="https://img.shields.io/badge/python-3.7+ | PyPy-blue.svg"></a>
        <img alt="Size" src="https://img.shields.io/github/languages/code-size/xiver-org/tnotify">
        <a href="https://pypi.org/project/tnotify/"><img alt="Pypi version" src="https://img.shields.io/pypi/l/tnotify?color=orange"></a>
    </p>
    <p align="center">
        <a href="https://github.com/xiver-org/tnotify/actions/workflows/tests.yml"><img alt="Testing status" src="https://github.com/xiver-org/tnotify/actions/workflows/tests.yml/badge.svg?branch=master"></a>
        <a href="https://github.com/xiver-org/tnotify/actions/workflows/linting.yml"><img alt="Linting" src="https://github.com/xiver-org/tnotify/actions/workflows/linting.yml/badge.svg?branch=master"></a>
        <a href='https://tnotify.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/tnotify/badge/?version=latest' alt='Documentation Status' /></a>
    </p>

=========

**Tnotify** was created to quickly notify the developer about the problems that arose in his project.

Do not like to look at the logs? Want to find out about the errors as soon as possible? Do not want to receive the Bug Reports sea?
Then this library is for you! With it, you can receive the notifications about the problems in Telegram as quickly as possible!

!! **CAUTION** !! This library is currently under development. Its use is not recommended in production versions of applications

.. end-of-readme-intro

Installation
^^^^^^^^^^^^

**From PyPi**::

    pip install tnotify

**From source** 

*Dependencies*:

* `poetry`

::

    $ git clone https://github.com/xiver-org/tnotify.git; cd tnotify-master
    $ poetry run build; cd dist
    $ pip install $(ls -Art | tail -n 1)


.. end-of-readme-basic-usage
