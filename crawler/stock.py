import json
import os
from datetime import date, datetime, timedelta
from typing import Dict, Optional

import pandas as pd

from crawler.utils.configs import SEARCH_DATE_LIMIT
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS
from crawler.utils.errors import FutureDateError
from crawler.utils.files import mkdir_if_not_exists
from crawler.utils.paths import get_stockprice_path


def get_stock_prices(corpcode: str) -> Dict[date, int]:
    assert isinstance(corpcode, str)

    ret = {}
    oldest_date = get_oldest_date(corpcode)
    oldest_date = max(oldest_date, SEARCH_DATE_LIMIT)
    get_stock_price(corpcode, get_oldest_date(corpcode))

    curr_date = get_latest_date()
    while True:
        ret[curr_date] = load_price_data(corpcode, curr_date)
        curr_date -= timedelta(days=1)
        if oldest_date > curr_date:
            break
    return ret


def get_latest_date() -> date:
    url = "https://finance.naver.com/item/sise_day.nhn?code={}&page=1".format(CORPCODE_SAMSUNG_ELECTRONICS)
    return datetime.strptime(pd.read_html(url)[0].dropna().날짜.array[0], "%Y.%m.%d").date()


def get_oldest_date(corpcode) -> date:
    url = "https://finance.naver.com/item/sise_day.nhn?code={}&page=9999".format(corpcode)
    date_as_str = pd.read_html(url)[0].dropna().날짜.array[-1]
    return datetime.strptime(date_as_str, "%Y.%m.%d").date()


def load_price_data(corpcode: str, target_date: date) -> int:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)

    stockprice_path = get_stockprice_path(corpcode, target_date)
    return json.load(open(stockprice_path, 'r'))


def save_price_data(corpcode: str, target_date: date, price: Optional[int]) -> None:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)
    assert isinstance(price, int) or price is None

    stockprice_path = get_stockprice_path(corpcode, target_date)
    mkdir_if_not_exists(os.path.dirname(stockprice_path))
    json.dump(price, open(stockprice_path, 'w'))


def internal_get_stock_price(corpcode: str, target_date: date) -> Optional[int]:
    if target_date > get_latest_date():
        raise FutureDateError(f'latest date: [{get_latest_date()}]. requested: [{target_date}]')

    ret = {}
    page = 1
    terminate = False
    previous_date: Optional[date] = None

    while True:
        if terminate:
            break
        url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}".format(corpcode, page)
        for idx, each in pd.read_html(url)[0].dropna().iterrows():
            each_date = datetime.strptime(each.날짜, "%Y.%m.%d").date()
            price = None
            if previous_date is not None and (previous_date - each_date) > timedelta(days=1):
                curr_holiday = previous_date - timedelta(days=1)
                while True:
                    if curr_holiday <= each_date:
                        break
                    save_price_data(corpcode, curr_holiday, None)
                    curr_holiday -= timedelta(days=1)
            if not os.path.exists(get_stockprice_path(corpcode, each_date)):
                price = int(each.종가)
                save_price_data(corpcode, each_date, price)
            if price is None:
                price = load_price_data(corpcode, each_date)
            if each_date == target_date:
                return price
            if each_date < target_date or each_date in ret:
                terminate = True
                break
            previous_date = each_date
        page += 1
    return None


def get_stock_price(corpcode: str, target_date: date) -> Optional[int]:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)

    stockprice_path = get_stockprice_path(corpcode, target_date)
    if os.path.exists(stockprice_path):
        return load_price_data(corpcode, target_date)

    stockprice = internal_get_stock_price(corpcode, target_date)
    return stockprice
