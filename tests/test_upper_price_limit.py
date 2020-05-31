from datetime import date

from crawler.upper_price_limit import get_upperpricelimit_histories, get_upper_price_limit, get_rounded_down, get_tick_size
from crawler.utils.consts import CORPCODE_BLOSSOM_MEDIA_COSMETICS, CORPCODE_KCS, CORPCODE_KNN


def test_get_upperpricelimit_histories1():
    actual = get_upperpricelimit_histories(CORPCODE_BLOSSOM_MEDIA_COSMETICS)
    assert date(2020, 5, 22) in actual
    assert date(2020, 5, 20) in actual


def test_get_upperpricelimit_histories2():
    actual = get_upperpricelimit_histories(CORPCODE_KCS)
    assert date(2020, 5, 19) in actual


def test_get_upperpricelimit_histories3():
    actual = get_upperpricelimit_histories(CORPCODE_KNN)
    assert date(2020, 5, 29) in actual


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
