from crawler.corp import get_krx_corplist


def test_get_krx_corplist():
    actual = get_krx_corplist()
    assert {'name': '삼성전자', 'code': '005930'} in actual
    assert {'name': '삼성전자우', 'code': '005935'} in actual
