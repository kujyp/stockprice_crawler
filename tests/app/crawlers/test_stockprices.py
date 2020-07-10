from datetime import datetime

from app.models.corp import Corp
from app.models.stockprice import Stockprice
from crawler.utils.consts import CORPCODE_SAMSUNG_ELECTRONICS, CORPCODE_BLOSSOM_MEDIA_COSMETICS


def test_crawlers_stockprices(client):
    corp1 = Corp(
        corpcode=CORPCODE_SAMSUNG_ELECTRONICS,
        corpname="삼성전자",
    ).save()
    Corp(
        corpcode=CORPCODE_BLOSSOM_MEDIA_COSMETICS,
        corpname="블러썸엠앤씨",
    ).save()

    resp = client.get(
        "/api/crawlers/stockprices/?from_date=2020-07-03&to_date=2020-07-04",
    )

    assert len(resp.json) == 2 * 2
    corp1_stockprices = Stockprice.query \
        .filter_by(corp_id=corp1.id) \
        .order_by(Stockprice.target_date) \
        .all()
    assert corp1_stockprices[0].target_date == datetime(2020, 7, 3)
    assert corp1_stockprices[0].price == 53600
    assert corp1_stockprices[0].is_holiday is False
    assert corp1_stockprices[1].target_date == datetime(2020, 7, 4)
    assert corp1_stockprices[1].is_holiday is True
    assert corp1_stockprices[1].price is None
