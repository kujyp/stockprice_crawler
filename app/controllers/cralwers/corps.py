from flask import Blueprint, jsonify
from flask_restful import marshal

from app.controllers.fields.corp import corp_fields
from app.models import db
from app.models.corp import Corp
from crawler.corp import get_krx_corplist

crawlers_corps_api = Blueprint('api.crawlers.corps', __name__)


@crawlers_corps_api.route("/", methods=['GET'])
def crawl_corps():
    appended = []
    corplist = get_krx_corplist()

    existings = Corp.query.all()
    corpcodes = set([each.corpcode for each in existings])
    for each in corplist:
        if each['code'] not in corpcodes:
            corp = Corp(
                corpcode=each['code'],
                corpname=each['name'],
            )
            db.session.add(corp)
            appended.append(corp)
    db.session.commit()
    return jsonify(marshal(appended, corp_fields))
