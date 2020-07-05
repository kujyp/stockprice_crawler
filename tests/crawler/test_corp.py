from crawler.corp import get_krx_corplist


def test_get_krx_corplist():
    actual = get_krx_corplist()
    assert {'name': '삼성전자', 'code': '005930'} in actual
    assert {'name': '삼성전자우', 'code': '005935'} in actual
    assert {'name': '일양약품우', 'code': '007575'} in actual
    assert {'name': '고려산업', 'code': '002140'} in actual
    assert {'name': 'KNN', 'code': '058400'} in actual
    assert {'name': '와이엔텍', 'code': '067900'} in actual
