from unittest import TestCase
from lambda_function import lambda_handler


class TestLambdaFunction(TestCase):
    def setUp(self):
        pass

    def test_success(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "1800",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        response = lambda_handler(data, None)
        print(response)

