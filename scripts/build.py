from os import system


def build() -> None:
    system("python setup.py sdist")
