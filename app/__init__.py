import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.controllers.cralwers.corps import crawlers_corps_api
from app.controllers.cralwers.stockprices import crawlers_stockprices_api
from app.controllers.home import home_api
from app.controllers.corps import corps_api


def create_app(**kwargs):
    app = Flask(__name__)

    load_dotenv(find_dotenv())
    os.environ.update(kwargs)
    app.config.from_mapping(os.environ)

    app.register_blueprint(home_api, url_prefix='/')
    app.register_blueprint(corps_api, url_prefix='/api/corps')
    app.register_blueprint(crawlers_corps_api, url_prefix='/api/crawlers/corps')
    app.register_blueprint(crawlers_stockprices_api, url_prefix='/api/crawlers/stockprices')

    from app.models import db
    db.init_app(app)
    Migrate(app, db)
    from app.utils.errors import init_errorhandler
    init_errorhandler(app)

    return app
