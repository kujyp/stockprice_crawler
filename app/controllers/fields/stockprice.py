from flask_restful import fields

from app.controllers.fields.corp import corp_fields

stockprice_fields = {
    'id': fields.Integer,
    'target_date': fields.String,
    'corp': fields.Nested(corp_fields),
    'is_holiday': fields.Boolean,
    'price': fields.Integer,

    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}
