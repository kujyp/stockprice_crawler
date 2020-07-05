from flask_restful import fields

corp_fields = {
    'id': fields.Integer,
    'corpname': fields.String,
    'corpcode': fields.String,

    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}
