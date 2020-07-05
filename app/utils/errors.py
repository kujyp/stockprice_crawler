from typing import List

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.utils.codes import CODE_INVALID_ARGUMENT, CODE_INVALID_ARGUMENTS


def make_response_with_exception(e: HTTPException):
    if isinstance(e, InvalidArgumentError):
        return dict(
            errorcode=e.errorcode,
            invalid_keyname=e.invalid_keyname,
            message=e.description,
        ), e.code
    if isinstance(e, InvalidArgumentsError):
        return dict(
            errorcode=e.errorcode,
            invalid_keynames=e.invalid_keynames,
            message=e.description,
        ), e.code

    raise NotImplementedError


def init_errorhandler(app):
    @app.errorhandler(StockpriceException)
    def handle_stockprice_error(error):
        result = {
            "message": error.description,
        }
        if error.internal_status_code:
            result["internal_status_code"] = error.internal_status_code
        response = jsonify(result)
        response.status_code = error.code
        return response


class StockpriceException(HTTPException):
    def __init__(self, description=None, response=None, internal_status_code=None):
        if description is None:
            description = f"{self.__class__.name}"
        super().__init__(description, response)
        self.internal_status_code = internal_status_code


class DataNotFoundError(StockpriceException):
    code = 404

    def __init__(self, description=None, response=None, internal_status_code=None):
        if description is None:
            description = "Data not found."
        super().__init__(description, response, internal_status_code)


class BadRequestError(StockpriceException):
    code = 400


class InvalidArgumentError(StockpriceException):
    code = 400
    errorcode = CODE_INVALID_ARGUMENT

    def __init__(self, invalid_keyname=None, additional_message=None, response=None):
        assert invalid_keyname, "invalid_keyname required."
        if additional_message is None:
            additional_message = "Invalid argument."
        self.invalid_keyname = invalid_keyname
        self.additional_message = additional_message
        description = f"Invalid argument [{invalid_keyname}]. {additional_message}".strip()
        super().__init__(description, response)


class InvalidArgumentsError(StockpriceException):
    code = 400
    errorcode = CODE_INVALID_ARGUMENTS

    def __init__(self, invalid_keynames: List[str] = None, additional_message=None, response=None):
        assert invalid_keynames, "invalid_keynames required."
        assert isinstance(invalid_keynames, list), "invalid_keynames should be list"
        if additional_message is None:
            additional_message = "Invalid arguments."
        self.invalid_keynames = invalid_keynames
        self.additional_message = additional_message
        description = f"Invalid argument [{invalid_keynames}]. {additional_message}".strip()
        super().__init__(description, response)


class UnauthorizedError(StockpriceException):
    code = 401

    def __init__(self, description=None, response=None, internal_status_code=None):
        if description is None:
            description = "Unauthorized."
        super().__init__(description, response, internal_status_code)


class XmlparserServerError(StockpriceException):
    code = 500


class DuplicatedDataError(StockpriceException):
    code = 400


class DataTooLongError(StockpriceException):
    code = 400


class InvalidRelationDataError(StockpriceException):
    code = 400


class UnknownDatabaseError(StockpriceException):
    code = 400


class UnknownError(StockpriceException):
    code = 400


class UnexpectedError(StockpriceException):
    code = 500
