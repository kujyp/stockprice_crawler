import sqlalchemy.exc
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy

from app.models.timeutils import now_utc
from app.utils.errors import DataNotFoundError, InvalidRelationDataError, UnknownDatabaseError, \
    InvalidArgumentError, make_response_with_exception, UnexpectedError

db = SQLAlchemy(session_options={
    "autoflush": False
})


def get_or_404(model_clazz, pk):
    instance = get_or_none(model_clazz, pk)
    if instance is None:
        raise DataNotFoundError(
            "{} {} Not found".format(model_clazz.__name__, pk))

    return instance


def get_or_assert(model_clazz, pk):
    instance = get_or_none(model_clazz, pk)
    assert instance is not None, ("{} {} Not found".format(model_clazz.__name__, pk))
    return instance


def get_or_none(model_clazz, pk):
    return model_clazz.query.filter_by(id=pk).first()


def get_colname_with_1406_error_message(msg: str) -> str:
    assert msg.startswith("Data too long for column \'")
    prefixremoved: str = msg[len("Data too long for column \'"):]
    return prefixremoved[:prefixremoved.find('\'')]


def get_colname_with_1062_error_message(msg: str) -> str:
    assert msg.startswith("Duplicate entry \'")
    prefixremoved: str = msg[len("Duplicate entry \'"):]
    entryremoved = prefixremoved[prefixremoved.find('\'') + 1:]
    assert entryremoved.startswith(" for key \'")
    prefixremoved2 = entryremoved[len(" for key \'"):]
    return prefixremoved2[:prefixremoved2.find('\'')]


def abort_with_databaseerror(e):
    if e.orig.args[0] == 1406:
        if not e.orig.args[1].startswith("Data too long for column \'"):
            raise UnexpectedError(e.orig.args[1])
        invalid_keyname = get_colname_with_1406_error_message(e.orig.args[1])
        abort(make_response_with_exception(InvalidArgumentError(
            invalid_keyname=invalid_keyname,
            additional_message=e.orig.args[1]
        )))
    if e.orig.args[0] == 1452:
        raise InvalidRelationDataError(str(e.orig.args[1]))
    elif e.orig.args[0] == 1062:
        if not e.orig.args[1].startswith("Duplicate entry \'"):
            raise UnexpectedError(e.orig.args[1])

        invalid_keyname = get_colname_with_1062_error_message(e.orig.args[1])
        abort(make_response_with_exception(InvalidArgumentError(
            invalid_keyname=invalid_keyname,
            additional_message=e.orig.args[1]
        )))
    raise UnknownDatabaseError(str(e.orig))


class TimestampMixin:
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=now_utc())
    updated_at = db.Column(db.DateTime,
                           nullable=True,
                           onupdate=now_utc())


class BaseModelMixin:
    def validates_or_assert(self):
        if False:
            raise InvalidArgumentError('key', 'invalid [key]')

    def save(self):
        self.validates_or_assert()
        try:
            db.session.add(self)
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            print(str(e))
            db.session.rollback()
            abort_with_databaseerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e
        return self

    def update(self):
        self.validates_or_assert()
        try:
            db.session.merge(self)
            db.session.commit()
        except sqlalchemy.exc.DatabaseError as e:
            print(str(e))
            db.session.rollback()
            abort_with_databaseerror(e)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            raise e
