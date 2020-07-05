def test_crawlers_corps(client):
    resp = client.get(
        "/api/crawlers/corps/",
    )

    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    assert len(resp.json) > 0
    corpcodes = [each['corpcode'] for each in resp.json]
    assert '005930' in corpcodes
    assert '005935' in corpcodes
    assert '007575' in corpcodes
    assert '002140' in corpcodes
    assert '058400' in corpcodes
    assert '067900' in corpcodes


def test_crawlers_corps_twice(client):
    resp1 = client.get(
        "/api/crawlers/corps/",
    )
    resp2 = client.get(
        "/api/crawlers/corps/",
    )

    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert isinstance(resp2.json, list)
    assert len(resp2.json) == 0
