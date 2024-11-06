.. raw:: html

   <p align="center">
        <h1 align="center">FrozenClass</h1>
        <h2 align="center">This library was created in order to be able to save classes with a single line, as well as load them!</h2>
    </p>

    <p align="center">
        <a href="https://pypi.python.org/pypi/frozenclass"><img alt="Pypi version" src="https://img.shields.io/pypi/v/frozenclass.svg"></a>
        <a href="https://pypi.python.org/pypi/frozenclass"><img alt="Python versions" src="https://img.shields.io/badge/python-3.7+ | PyPy-blue.svg"></a>
        <img alt="Size" src="https://img.shields.io/github/languages/code-size/GigantPro/frozenclass">
        <a href="https://pypi.org/project/frozenclass/"><img alt="Pypi version" src="https://img.shields.io/pypi/l/frozenclass?color=orange"></a>
    </p>
    <p align="center">
        <a href="https://github.com/GigantPro/frozenclass/actions/workflows/tests.yml"><img alt="Testing status" src="https://github.com/GigantPro/frozenclass/actions/workflows/tests.yml/badge.svg?branch=main"></a>
        <a href="https://github.com/GigantPro/frozenclass/actions/workflows/linting.yml"><img alt="Linting" src="https://github.com/GigantPro/frozenclass/actions/workflows/linting.yml/badge.svg?branch=main"></a>
        <a href='https://frozenclass.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/frozenclass/badge/?version=latest' alt='Documentation Status' /></a>
    </p>

=========

**Frozenclass** is a library for convenient storage of class variables and their subsequent loading in Python.

Have you ever used self-written methods like `save_as_file` or `load_from_file` that took up a lot of space and were pretty hard to write?
**Forget**! The **frozenclass** library will take care of that! Now use just one function instead of that unwieldy code!

Also, this library, using its decorator, will be able to **automatically** save the changes made to the class, and then, the next time the class object is created, load them from a file and install them in the class!


.. end-of-readme-intro

Installation
^^^^^^^^^^^^

**From PyPi**::

    pip install frozenclass

**From source** 

*Dependencies*:

* `poetry`

::

    $ git clone https://github.com/GigantPro/frozenclass.git; cd frozenclass-main
    $ poetry run build; cd dist
    $ pip install $(ls -Art | tail -n 1)

Quick start
-------------

* `Installation`_
* `Main functions and classes`_
* `Basic usage`_

Main functions and classes
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `frozenclass` library has a main module - **DataController**. It is a program API and can provide you with almost all the functionality of the library.

You can also import the **AutoFreeze** function from the `frozenclass` library. This function should be used as a class decorator to automatically load/save a class.

!! **CAUTION** !! do not use more than one instance of the class with this decorator in your code. when loading or saving **only one instance of the class that was last modified will be used!**


Basic usage
^^^^^^^^^^^

* `DataController`_
* `AutoFreeze`_

First of all, you need to import the library.
If you want to control the save/load process manually, then use **DataController**::

    from frozenclass import DataController

If you are ready to trust automation, then you should import **AutoFreeze**::

    from frozenclass import AutoFreeze

DataController
--------------

`DataController` has several methods, but as a quick start, I will only cover two: **freeze_class** and **load_save**.

To test both functions, we need to create a test class::

    class TestClass:
        a: int = 10
        def __init__(self, b: str) -> None:
            self.b = b

Now we need to create an instance of the `DataController` class. As input, it takes the path to the save folders (`saves_folder_path: str`)::

    controller = DataController('saves')

Now we can work with saves through the controller. In order for us to save a class object, we must create it, and then put it as an argument in the controller's `.freeze_class` method, which will return us the name of the save, by which we can then load our class::

    test_obj = TestClass('qwerty')
    save_name = controller.freeze_class(test_obj)

Imagine that we made the next launch of the program with a known save name (how do we know it? Alternatively, you can save it in a file, or set it static by passing it as the second parameter to the method). Let's load an instance of the class::

    loaded_obj = controller.load_save(save_name)

To do this, we must use the controller's `.load_save` method, which takes `save_name: str` as input (the name that was assigned to the save automatically or manually).::

    loaded_obj = controller.load_save(save_name)

Now the `loaded_obj` variable will contain all the variables of the original object, except for some (see the detailed description of the method)

``And here is the entire code of the example``::

    from frozenclass import DataController

    class TestClass:
        a: int = 10

        def __init__(self, b: str) -> None:
            self.b = b

    controller = DataController('saves')

    test_obj = TestClass('qwerty')
    save_name = controller.freeze_class(test_obj)

    loaded_obj = controller.load_save(save_name)


AutoFreeze
----------

Okay, now let's imagine that you want to automate the process and not spend extra lines of code and time working with the controller.

For example, let's remake the code from the previous example a bit::

    from frozenclass import AutoFreeze, DataController

Import both `AutoSave` and `DataController` (it is only needed to check the result)

Further, some changes were also made to the class::

    @AutoFreeze()
    class TestClass:
        a: int = 10
        __name__ = 'TestClassExample'

        def __init__(self, b: str) -> None:
            self.b = b

First of all, we need to decorate our class.

Further, in order for the decorator to work correctly and there were no errors, you need to specify the `__name__` attribute (then you can use it to manually load the save)

Leave the rest of the class creation the same.


We also need to rewrite part of the simulated unloading and checking save/load

We create an instance of the test class and simulate the work by changing the parameter `a`::

    test_obj = TestClass('qwerty')
    test_obj.a = 100

Actually, after making any changes to a class instance, it is saved in a file and the next time a new instance is created, it will inherit all the changed parameters of the previous (maybe no longer existing) class instance::

    controller = DataController('saves')
    loaded_obj_save_loaded = controller.load_save('TestClassExample')

    new_test_obj = TestClass('qwerty')

    loaded_obj_save_loaded.__dict__ == new_test_obj.__dict__  # True

``And here is the entire code of the example``::

    from frozenclass import AutoFreeze, DataController


    @AutoFreeze()
    class TestClass:
        a: int = 10
        __name__ = 'TestClassExample'

        def __init__(self, b: str) -> None:
            self.b = b


    test_obj = TestClass('qwerty')
    test_obj.a = 100

    controller = DataController('saves')
    loaded_obj_save_loaded = controller.load_save('TestClassExample')

    new_test_obj = TestClass('qwerty')

    loaded_obj_save_loaded.__dict__ == new_test_obj.__dict__



Conclusion
^^^^^^^^^^

Well, this was a small introductory course for a quick start with this library and understanding its functionality. You can read more in the documentation.

.. end-of-readme-basic-usage

