from flask import Blueprint, request, abort
from flask_restful import reqparse, Resource, marshal_with, Api

from app.controllers.fields.corp import corp_fields
from app.models import get_or_404
from app.models.corp import Corp


corp_reqparser = reqparse.RequestParser()
corp_reqparser.add_argument(
    'corpname', type=str, trim=True,
    location=['form', 'json'],
    required=True, nullable=False,
    help='corpname required'
)
corp_reqparser.add_argument(
    'corpcode', type=str, trim=True,
    location=['form', 'json'],
    required=True, nullable=False,
    help='corpcode required'
)


class CorpListResource(Resource):
    def __init__(self):
        super().__init__()

    @marshal_with(corp_fields)
    def get(self):
        return Corp.query.all()

    @marshal_with(corp_fields)
    def post(self):
        args = corp_reqparser.parse_args()

        corp = Corp(**args)
        corp.save()
        return corp, 201


class CorpResource(Resource):
    @marshal_with(corp_fields)
    def get(self, pk):
        return get_or_404(Corp, pk)

    @marshal_with(corp_fields)
    def put(self, pk):
        args = None
        if request.is_json:
            args = request.json
        elif request.form:
            args = request.form
        if args is None:
            abort(400, "Try as json or form request")

        corp = get_or_404(Corp, pk)

        for key, value in args.items():
            if value is None:
                continue

            setattr(corp, key, value)

        corp.update()
        return get_or_404(Corp, pk)

    def delete(self, pk):
        corp = get_or_404(Corp, pk)
        corp.delete()
        return '', 204


corps_api = Blueprint('api.corps', __name__)
api = Api(corps_api)
api.add_resource(
    CorpListResource,
    '',
    endpoint='corps'
)

api.add_resource(
    CorpResource,
    '/<int:pk>',
    endpoint='corp'
)
