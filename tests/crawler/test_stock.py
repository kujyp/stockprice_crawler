from datetime import date, timedelta

from app.models.stockprice import StockpriceSimple
from crawler.stock import get_latest_date, get_oldest_date, get_prevday_stock_price, get_stockprices
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS, CORPCODE_KCS, CORPCODE_Y_ENTEC, CORPCODE_KNN


def test_get_oldest_date():
    assert get_oldest_date(CORPCODE_SAMSUNG_ELECTRONICS) == date(1996, 6, 25)
    assert get_oldest_date(CORPCODE_KCS) == date(2010, 4, 14)


def test_get_latest_date():
    assert date.today() - timedelta(days=5) <= get_latest_date() <= date.today() + timedelta(days=5)


def test_get_stock_prices1():
    actual = get_stockprices(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 28))
    assert actual[date(2020, 5, 29)] == StockpriceSimple(CORPCODE_SAMSUNG_ELECTRONICS, date(2020, 5, 29), 50700)
    assert date(2005, 1, 10) not in actual
    assert date(1996, 6, 25) not in actual


def test_get_stock_prices2():
    actual = get_stockprices(CORPCODE_Y_ENTEC, date(2019, 3, 21), date(2019, 3, 22))
    assert len(actual) == 2
    assert actual[date(2019, 3, 22)] == StockpriceSimple(CORPCODE_Y_ENTEC, date(2019, 3, 22), 7880)
    assert actual[date(2019, 3, 21)] == StockpriceSimple(CORPCODE_Y_ENTEC, date(2019, 3, 21), 6880)


def test_get_stock_prices3():
    actual = get_stockprices(CORPCODE_KNN, date(2020, 5, 27))
    assert actual[date(2020, 5, 29)] == StockpriceSimple(CORPCODE_KNN, date(2020, 5, 29), 1660)
    assert actual[date(2020, 5, 28)] == StockpriceSimple(CORPCODE_KNN, date(2020, 5, 28), 1280)


def test_get_prevday_stock_price():
    assert get_prevday_stock_price('223250', date(2020, 5, 22)) is None
