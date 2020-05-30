import os


def mkdir_if_not_exists(target: str):
    assert isinstance(target, str)
    if not os.path.exists(target):
        os.makedirs(target)
