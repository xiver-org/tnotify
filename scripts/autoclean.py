from os import system


def autoclean():  # noqa: ANN201
    system("rm -rf dist")
    system("rm -rf tnotify.egg-info")
    system("rm -rf .pytest_cache")
    system("rm -rf saves")
    system(r"find . -name __pycache__ -exec rm -rf {} \;")
