from datetime import date, timedelta

import pytest

from crawler.stock import get_stock_prices, internal_get_stock_price, get_latest_date, get_oldest_date
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS, CORPCODE_KCS
from crawler.utils.errors import FutureDateError


def test_get_oldest_date():
    assert get_oldest_date(CORPCODE_SAMSUNG_ELECTRONICS) == date(1996, 6, 25)
    assert get_oldest_date(CORPCODE_KCS) == date(2010, 4, 14)


def test_get_latest_date():
    assert date.today() - timedelta(days=5) <= get_latest_date() <= date.today() + timedelta(days=5)


def test_get_stock_prices():
    actual = get_stock_prices(CORPCODE_SAMSUNG_ELECTRONICS)
    assert actual[date(2020, 5, 29)] == 50700
    assert actual[date(2005, 1, 10)] == 438000
    assert actual[date(1996, 6, 25)] == 67500


def test_internal_get_stock_price_with_futuredate():
    with pytest.raises(FutureDateError):
        internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2099, 1, 1))


def test_internal_get_stock_price():
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 29)) == 50700
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 24)) is None
    assert internal_get_stock_price(CORPCODE_SAMSUNG_ELECTRONICS, date(1996, 6, 25)) == 67500
