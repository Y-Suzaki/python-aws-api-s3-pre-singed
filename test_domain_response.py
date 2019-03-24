from unittest import TestCase
from domain_response import DomainException, BadRequestException, InternalError
from datetime import datetime, timezone

class TestDomainResponse(TestCase):
    def setUp(self):
        pass

    def test_aaa(self):
        print(datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f'))


    def test_bad_request(self):
        try:
            raise BadRequestException()
        except DomainException as ex:
            self.assertEqual(400, ex.to_json()['statusCode'])

    def test_internal_error(self):
        try:
            raise InternalError()
        except DomainException as ex:
            self.assertEqual(503, ex.to_json()['statusCode'])
