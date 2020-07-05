import os

from crawler.utils.paths import get_project_root


def test_get_project_root():
    assert '.git' in os.listdir(get_project_root())
