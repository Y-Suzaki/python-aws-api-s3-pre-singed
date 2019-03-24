from abc import ABCMeta, abstractmethod


class DomainResponse(metaclass=ABCMeta):
    @abstractmethod
    def to_json(self):
        pass


class DomainException(Exception, DomainResponse):
    @abstractmethod
    def to_json(self):
        pass


class Success(DomainResponse):
    def __init__(self, uri):
        self.uri = uri

    def to_json(self):
        return {'statusCode': 200, 'uri': self.uri}


class BadRequestException(DomainException):
    def to_json(self):
        return {'statusCode': 400, 'body': 'Bad Request.'}


class InternalError(DomainException):
    def to_json(self):
        return {'statusCode': 503, 'body': 'Internal Server Error.'}
