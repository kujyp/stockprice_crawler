from datetime import date, timedelta

import pytest

from crawler.stock import get_stock_prices, internal_get_stock_price, get_latest_date, get_oldest_date
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS, CORPCODE_KCS, CORPCODE_Y_ENTEC, CORPCODE_KNN
from crawler.utils.errors import FutureDateError


def test_get_oldest_date():
    assert get_oldest_date(CORPCODE_SAMSUNG_ELECTRONICS) == date(1996, 6, 25)
    assert get_oldest_date(CORPCODE_KCS) == date(2010, 4, 14)


def test_get_latest_date():
    assert date.today() - timedelta(days=5) <= get_latest_date() <= date.today() + timedelta(days=5)


def test_get_stock_prices1():
    actual = get_stock_prices(CORPCODE_SAMSUNG_ELECTRONICS)
    assert actual[date(2020, 5, 29)] == 50700
    assert date(2005, 1, 10) not in actual
    assert date(1996, 6, 25) not in actual


def test_get_stock_prices2():
    actual = get_stock_prices(CORPCODE_Y_ENTEC)
    assert actual[date(2019, 3, 22)] == 7880
    assert actual[date(2019, 3, 21)] == 6880


def test_get_stock_prices3():
    actual = get_stock_prices(CORPCODE_Y_ENTEC)
    assert actual[date(2019, 3, 22)] == 7880
    assert actual[date(2019, 3, 21)] == 6880


def test_get_stock_prices4():
    actual = get_stock_prices(CORPCODE_KNN)
    assert actual[date(2020, 5, 29)] == 1660
    assert actual[date(2020, 5, 28)] == 1280


def test_internal_get_stock_price_with_futuredate():
    with pytest.raises(FutureDateError):
        internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2099, 1, 1))


def test_internal_get_stock_price():
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 29)) == 50700
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 24)) is None
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(1996, 6, 25)) == 67500
