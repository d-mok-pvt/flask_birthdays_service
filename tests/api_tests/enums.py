from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"

class ResponseCode(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
