from app.models.corp import Corp


def test_get_stocks(client):
    corp1 = Corp(
        corpcode="1",
        corpname="a",
    ).save()
    corp2 = Corp(
        corpcode="2",
        corpname="b",
    ).save()

    resp = client.get(
        "/api/corps",
    )

    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    assert len(resp.json) == 2
    assert resp.json[0]['corpcode'] == corp1.corpcode
    assert resp.json[1]['corpcode'] == corp2.corpcode
