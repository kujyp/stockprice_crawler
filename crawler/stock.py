import json
import os
from datetime import date, datetime, timedelta
from typing import Dict, Optional, Any

import pandas as pd

from app.models.corp import get_corp_or_none
from app.models.stockprice import Stockprice, StockpriceSimple
from crawler.utils.configs import SEARCH_DATE_LIMIT
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS
from crawler.utils.files import mkdir_if_not_exists
from crawler.utils.paths import get_stockprice_path, get_oldest_path


cache = {
    'latest_date': None,
}


def internal_get_stock_price(
        corpcode: str,
        target_date: date,
        dynamic_price_tables: Dict[date, Any],
) -> Optional[int]:
    page = 1
    terminate = False
    previous_date: Optional[date] = None

    if target_date in dynamic_price_tables:
        return dynamic_price_tables[target_date]

    while True:
        if terminate:
            break
        url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}".format(corpcode, page)
        for idx, each in pd.read_html(url)[0].dropna().iterrows():
            each_date = datetime.strptime(each.날짜, "%Y.%m.%d").date()
            if previous_date is not None and (previous_date - each_date) > timedelta(days=1):
                curr_holiday = previous_date - timedelta(days=1)
                while True:
                    if curr_holiday <= each_date:
                        break
                    dynamic_price_tables[curr_holiday] = None
                    curr_holiday -= timedelta(days=1)
            price = int(each.종가)
            dynamic_price_tables[each_date] = price
            if each_date == target_date:
                return price
            if each_date < target_date:
                terminate = True
                break
            previous_date = each_date
        page += 1
    return None


def get_stockprices(corpcode: str, from_date: date, to_date: Optional[date] = None) -> Dict[date, StockpriceSimple]:
    assert isinstance(corpcode, str)
    assert isinstance(from_date, date)
    assert (to_date is None) or isinstance(to_date, date)

    dynamic_price_tables = {}

    oldest_date = max(get_oldest_date(corpcode), from_date)
    latest_date = min(get_latest_date(), to_date) if to_date is not None else get_latest_date()
    curr_date = oldest_date - timedelta(days=1)
    while True:
        curr_date += timedelta(days=1)
        if latest_date < curr_date:
            break

        if curr_date in dynamic_price_tables:
            continue
        dynamic_price_tables[curr_date] = internal_get_stock_price(corpcode, curr_date, dynamic_price_tables)

    ret = {}
    for eachdate, eachprice in dynamic_price_tables.items():
        ret[eachdate] = StockpriceSimple(
            target_date=eachdate,
            corpcode=corpcode,
            price=eachprice,
        )
    return ret


def get_latest_date() -> date:
    if cache['latest_date'] is not None:
        return cache['latest_date']

    url = "https://finance.naver.com/item/sise_day.nhn?code={}&page=1".format(CORPCODE_SAMSUNG_ELECTRONICS)
    cache['latest_date'] = datetime.strptime(pd.read_html(url)[0].dropna().날짜.array[0], "%Y.%m.%d").date()
    return cache['latest_date']


def get_oldest_date(corpcode) -> date:
    if os.path.exists(get_oldest_path(corpcode)):
        date_as_str = json.load(open(get_oldest_path(corpcode), 'r'))
        return datetime.strptime(date_as_str, "%Y.%m.%d").date()
    url = "https://finance.naver.com/item/sise_day.nhn?code={}&page=9999".format(corpcode)
    date_as_str = pd.read_html(url)[0].dropna().날짜.array[-1]

    mkdir_if_not_exists(os.path.dirname(get_oldest_path(corpcode)))
    json.dump(date_as_str, open(get_oldest_path(corpcode), 'w'))

    return datetime.strptime(date_as_str, "%Y.%m.%d").date()


def load_price_data(corpcode: str, target_date: date) -> Optional[int]:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)

    stockprice_path = get_stockprice_path(corpcode, target_date)
    try:
        json.load(open(stockprice_path, 'r'))
    except FileNotFoundError:
        return None


def save_price_data(corpcode: str, target_date: date, price: Optional[int]) -> None:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)
    assert isinstance(price, int) or price is None

    if price is None:
        Stockprice(target_date=target_date, stock=get_corp_or_none(corpcode), is_holiday=True).save()
    else:
        Stockprice(target_date=target_date, stock=get_corp_or_none(corpcode), price=price).save()


def get_prevday_stock_price(corpcode: str, target_date: date) -> Optional[int]:
    curr_date = target_date - timedelta(days=1)
    curr_price = None
    oldest_date = get_oldest_date(corpcode)
    oldest_date = max(oldest_date, SEARCH_DATE_LIMIT)
    while oldest_date <= curr_date:
        curr_price = get_stockprice(corpcode, curr_date)
        if curr_price is not None:
            break
        curr_date -= timedelta(days=1)
    return curr_price


def get_stockprice(corpcode: str, target_date: date) -> Optional[int]:
    return get_stockprices(corpcode, target_date, target_date)[target_date].price
