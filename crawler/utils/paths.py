import os
from datetime import date


def get_project_root() -> str:
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_stockprice_path(corpcode: str, target_date: date) -> str:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)

    return os.path.join(get_project_root(), 'data', 'prices', corpcode, f"{target_date.strftime('%Y%m%d')}.json")
