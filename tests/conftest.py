import os

import pytest

from app import create_app
from app.models import db


@pytest.fixture
def app(tmpdir):
    if "PYTEST_SQLALCHEMY_DATABASE_URI" in os.environ:
        db_uri = os.environ["PYTEST_SQLALCHEMY_DATABASE_URI"]
    else:
        db_uri = "mysql://root:1234@127.0.0.1:3306/test?charset=utf8"
        # db_uri = f"sqlite:///{tmpdir.strpath}/app.db"
    app = create_app(
        SQLALCHEMY_DATABASE_URI=db_uri,
    )
    with app.app_context():
        yield app.test_client()


@pytest.fixture
def init_db(app):
    from sqlalchemy.exc import OperationalError
    try:
        db.session.commit()
        db.drop_all()
        db.create_all()
    except OperationalError as e:
        pytest.exit(f"""Unable to connect local mysql server.
Hint: tools/run_mysql.sh
Error: [{str(e)}]""")

    yield db
    db.session.commit()
    db.drop_all()


@pytest.fixture
def client(app, init_db):
    yield app
