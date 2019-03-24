from unittest import TestCase
from domain_pre_signed import Domain
from domain_response import BadRequestException


class TestDomain(TestCase):
    """ domain_pre_signed.Domainのテストクラス
    """
    def setUp(self):
        pass

    def test_method_case_success(self):
        """ methodクエリパラメータの正常系テスト
        条件：クエリパラメータmethodにputが指定されていること
        結果：methodプロパティからputが取得できること
        """
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.method, 'put')

    def test_method_case_no_method(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_method_case_wrong_method(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "post"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_expire_case_success(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.expire, 300)

    def test_expire_case_no_expire(self):
        data = {
            "queryStringParameters": {
                "method": "put",
                "contenttype": "application/json"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_method_case_over_expire_limit(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "2000",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_content_type_case_success(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.content_type, 'application/json')

    def test_content_type_case_success_no_content_type(self):
        data = {
            "queryStringParameters": {
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        domain = Domain(data)
        self.assertTrue(domain.content_type is None)

    def test_key_case_success(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.bucket, 's3-bucket')
        self.assertTrue(domain.key.count('/') == 3 and domain.key.startswith('dir1/dir2/dir3/'))

    def test_key_case_success_min_length_directory(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.bucket, 's3-bucket')
        self.assertTrue(domain.key.count('/') == 0 and domain.key.__len__() == 22)

    def test_key_case_success_max_length_directory(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8/dir9/dir10/dir11/dir12/dir13/dir14/dir15/dir16/url"
            }
        }

        domain = Domain(data)
        self.assertEqual(domain.bucket, 's3-bucket')
        self.assertTrue(domain.key.count('/') == 16 and domain.key.startswith('dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8/dir9/dir10/dir11/dir12/dir13/dir14/dir15/dir16/'))

    def test_key_case_no_directory(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_key_case_too_short_directory(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_key_case_no_end_with_url(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/uri"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()

    def test_key_case_too_length_directory(self):
        data = {
            "queryStringParameters": {
                "contenttype": "application/json",
                "expire": "300",
                "method": "put"
            },
            "pathParameters": {
                "directory": "s3-bucket/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8/dir9/dir10/dir11/dir12/dir13/dir14/dir15/dir16/dir17/url"
            }
        }

        try:
            self.domain = Domain(data)
        except BadRequestException as e:
            return
        self.fail()
