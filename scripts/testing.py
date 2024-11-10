import sys
from os import system


def start_testing() -> None:  # ignore: ANN201
    system('pytest')
