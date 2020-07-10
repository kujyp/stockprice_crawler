from datetime import datetime

from flask import Blueprint, jsonify
from flask_restful import marshal, reqparse

from app.controllers.fields.stockprice import stockprice_fields
from app.models.corp import Corp
from app.models.stockprice import Stockprice
from crawler.stock import get_stockprices

crawlers_stockprices_api = Blueprint('api.crawlers.stockprices', __name__)


stockprice_reqparser = reqparse.RequestParser()
stockprice_reqparser.add_argument(
    'from_date', type=str, trim=True,
    location='args',
    required=True, nullable=False,
    help='from_date required'
)
stockprice_reqparser.add_argument(
    'to_date', type=str, trim=True,
    location='args',
    required=False,
)


@crawlers_stockprices_api.route("/", methods=['GET'])
def crawl_stockprices():
    args = stockprice_reqparser.parse_args()
    from_date = datetime.strptime(args.from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(args.to_date, "%Y-%m-%d").date() if args.to_date is not None else None

    corps = Corp.query.all()
    updateds = []
    for eachcorp in corps:
        stockprices = get_stockprices(eachcorp.corpcode, from_date, to_date)
        for each_date, each_stockprice in stockprices.items():
            if Stockprice.query.filter_by(target_date=each_stockprice.target_date).one_or_none() is not None:
                continue
            updateds.append(Stockprice(
                target_date=each_stockprice.target_date,
                corp=eachcorp,
                is_holiday=each_stockprice.is_holiday,
                price=each_stockprice.price,
            ).save())
    return jsonify(marshal(updateds, stockprice_fields))
