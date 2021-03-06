from datetime import date
from typing import List

from app.models.corp import CorpSimple
from crawler.stock import get_stockprice, get_prevday_stock_price, get_stockprices


def get_tick_size(price: int, is_kosdaq: bool) -> int:
    if price < 1000:
        return 1
    elif price < 5000:
        return 5
    elif price < 10000:
        return 10
    elif price < 50000:
        return 50
    elif price < 100000:
        return 100

    if is_kosdaq:
        return 100

    if price < 500000:
        return 500
    return 1000


def get_rounded_down(number: int, unit: int):
    assert isinstance(number, int)
    assert isinstance(unit, int)
    return int(number / unit) * unit


def get_upper_price_limit(prevday_price: int, is_kosdaq: bool) -> int:
    assert isinstance(prevday_price, int)
    assert isinstance(is_kosdaq, bool)

    # Ref: https://m.blog.naver.com/PostView.nhn?blogId=yahoosir&logNo=220651602149&proxyReferer=https:%2F%2Fwww.google.com%2F
    multiplied = int(prevday_price * 0.3)
    ticksize = get_tick_size(prevday_price, is_kosdaq)
    roundeddown = get_rounded_down(multiplied, ticksize)
    added = prevday_price + roundeddown
    return get_rounded_down(added, get_tick_size(added, is_kosdaq))


def is_upper_price_limit_diffences(nextday_price: int, today_price: int) -> bool:
    assert isinstance(nextday_price, int)
    assert isinstance(today_price, int)
    if nextday_price == get_upper_price_limit(today_price, True):
        return True
    if nextday_price == get_upper_price_limit(today_price, False):
        return True
    return False


def get_upperpricelimit_stocks(corplist: List[CorpSimple], target_date: date) -> List[CorpSimple]:
    assert isinstance(target_date, date)
    ret = []
    for eachcorp in corplist:
        if is_upperpricelimit(eachcorp.corpcode, target_date):
            ret.append(eachcorp)
    return ret


def is_upperpricelimit(corpcode: str, target_date: date) -> bool:
    assert isinstance(corpcode, str)
    assert isinstance(target_date, date)

    price = get_stockprice(corpcode, target_date)
    prevday_price = get_prevday_stock_price(corpcode, target_date)
    if price is None or prevday_price is None:
        return False
    return is_upper_price_limit_diffences(price, prevday_price)


def get_upperpricelimit_histories(corpcode: str, search_date_limit: date) -> List[date]:
    assert isinstance(corpcode, str)
    assert isinstance(search_date_limit, date)

    ret = []

    prices = get_stockprices(corpcode, search_date_limit)

    nextday_date = None
    nextday_price = None
    for key_date, val in prices.items():
        price = val.price
        if nextday_date is None or nextday_price is None:
            nextday_date = key_date
            nextday_price = price
            continue
        if val.is_holiday:
            continue
        if is_upper_price_limit_diffences(nextday_price, price):
            ret.append(nextday_date)
        nextday_date = key_date
        nextday_price = price

    return ret
