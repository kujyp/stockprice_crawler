from datetime import date

from crawler.upper_price_limit import get_upperpricelimit_histories, get_upper_price_limit, get_rounded_down, get_tick_size, \
    get_upperpricelimit_stocks
from crawler.utils.consts import CORPCODE_BLOSSOM_MEDIA_COSMETICS, CORPCODE_KCS, CORPCODE_KNN


def test_get_upperpricelimit_histories1(mocker):
    mocker.patch(
        "crawler.stock.SEARCH_DATE_LIMIT",
        date(2019, 4, 1),
    )
    actual = get_upperpricelimit_histories(CORPCODE_BLOSSOM_MEDIA_COSMETICS)
    assert date(2020, 5, 22) in actual
    assert date(2020, 5, 20) in actual


def test_get_upperpricelimit_histories2():
    actual = get_upperpricelimit_histories(CORPCODE_KCS)
    assert date(2020, 5, 19) in actual


def test_get_upperpricelimit_histories3():
    actual = get_upperpricelimit_histories(CORPCODE_KNN)
    assert date(2020, 5, 29) in actual


def test_get_upperpricelimit_stocks1():
    actual = get_upperpricelimit_stocks(date(2020, 5, 29))
    assert {'name': 'KNN', 'code': '058400'} in actual
    assert {'name': '고려산업', 'code': '002140'} in actual
    assert {'name': '에이루트', 'code': '096690'} not in actual


def test_get_upperpricelimit_stocks2():
    actual = get_upperpricelimit_stocks(date(2020, 5, 28))
    assert {'name': '피앤씨테크', 'code': '237750'} in actual
    assert {'name': '일양약품', 'code': '007570'} in actual
    assert {'name': '일양약품우', 'code': '007575'} in actual


def test_get_upperpricelimit_stocks3():
    actual = get_upperpricelimit_stocks(date(2020, 5, 27))
    assert {'name': '티비에이치글로벌', 'code': '084870'} in actual
    assert {'name': '지니뮤직', 'code': '043610'} in actual
    assert {'name': '유니슨', 'code': '018000'} in actual
    assert {'name': '라파스', 'code': '214260'} in actual
    assert {'name': '티플랙스', 'code': '081150'} in actual
    assert {'name': '인포마크', 'code': '175140'} in actual


def test_get_upperpricelimit_stocks4():
    actual = get_upperpricelimit_stocks(date(2020, 5, 21))
    assert {'name': '로보로보', 'code': '215100'} in actual
    assert {'name': '비디아이', 'code': '148140'} in actual
    assert {'name': '동국S&C', 'code': '100130'} in actual
    assert {'name': '글로벌에스엠', 'code': '900070'} in actual


def test_get_rounded_down():
    assert get_rounded_down(475, 50) == 450
    assert get_rounded_down(475, 100) == 400


def test_get_tick_size():
    assert get_tick_size(792000, False) == 1000


def test_get_upper_price_limit():
    assert get_upper_price_limit(505, True) == 656
    assert get_upper_price_limit(3490, True) == 4535
    assert get_upper_price_limit(1280, True) == 1660
    assert get_upper_price_limit(50400, True) == 65500
    assert get_upper_price_limit(109500, False) == 142000
    assert get_upper_price_limit(792000, False) == 1029000
