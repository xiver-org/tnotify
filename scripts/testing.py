import sys
from os import system


def start_testing() -> None:  # ignore: ANN201
    system('pytest')

    platform = sys.platform
    if platform == 'win32':
        system('rmdir /a test_saves')
    else:
        system('rm -rf test_saves')
