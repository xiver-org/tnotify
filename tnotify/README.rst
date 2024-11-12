Tnotify
=======

The python lib for fast telegram notifications.

.. image:: https://img.shields.io/pypi/v/tnotify.svg
   :target: https://pypi.python.org/pypi/tnotify
   :alt: Pypi version

.. image:: https://img.shields.io/badge/python-3.7+ | PyPy-blue.svg
   :target: https://pypi.python.org/pypi/tnotify
   :alt: Python versions

.. image:: https://img.shields.io/github/languages/code-size/xiver-org/tnotify
   :alt: Size

.. image:: https://img.shields.io/pypi/l/tnotify?color=orange
   :target: https://pypi.org/project/tnotify/
   :alt: License

.. image:: https://github.com/xiver-org/tnotify/actions/workflows/tests.yml/badge.svg?branch=master
   :target: https://github.com/xiver-org/tnotify/actions/workflows/tests.yml
   :alt: Testing status

.. image:: https://github.com/xiver-org/tnotify/actions/workflows/linting.yml/badge.svg?branch=master
   :target: https://github.com/xiver-org/tnotify/actions/workflows/linting.yml
   :alt: Linting

.. image:: https://readthedocs.org/projects/tnotify/badge/?version=latest
   :target: https://tnotify.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


=========

**Tnotify** was created to quickly notify the developer about the problems that arose in his project.

Do not like to look at the logs? Want to find out about the errors as soon as possible? Do not want to receive the Bug Reports sea?
Then this library is for you! With it, you can receive the notifications about the problems in Telegram as quickly as possible!

!! **CAUTION** !! This library is currently under development. Its use is not recommended in production versions of applications

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

