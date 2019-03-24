from domain_response import BadRequestException
from datetime import datetime, timezone
from logger.domain_logger import DomainLogger


class Domain:
    """ Domainの管理を行うクラス
    """
    def __init__(self, event):
        """ Lambda FunctionのEventから、Domainのデータ構造に変換
        :param event: Lambda function1から渡されるEventクラス
        """
        self.logger = DomainLogger.get_logger()

        self._method = Domain._extract_method(event['queryStringParameters'])
        self._expire = Domain._extract_expire(event['queryStringParameters'])
        self._content_type = Domain._extract_content_type(event['queryStringParameters'])
        self._bucket, self._key_prefix = Domain._extract_upload_path(event['pathParameters'])
        self._file_name = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')

    @property
    def method(self):
        return self._method

    @property
    def expire(self):
        return self._expire

    @property
    def content_type(self):
        return self._content_type

    @property
    def bucket(self):
        return self._bucket

    @property
    def key(self):
        return '{}{}'.format(self._key_prefix, self._file_name)

    def is_content_type(self):
        return False if self.content_type is None else True

    @staticmethod
    def _extract_method(queries):
        """ methodクエリパラメータを抽出＆チェックする関数
        条件：必須パラメータ、putのみ許可

        :param queries: クエリパラメータのDictionary
        :return: putの固定文字列
        :raise: BadRequestException
        """
        if 'method' not in queries or queries['method'] != 'put':
            raise BadRequestException()
        return 'put'

    @staticmethod
    def _extract_expire(queries):
        """expireクエリパラメータを抽出＆チェックする関数
        条件：必須パラメータ、10～1800秒の間のみ許可

        :param queries: クエリパラメータのDictionary
        :return: expireの値
        :raise: BadRequestException
        """
        if 'expire' not in queries:
            raise BadRequestException()
        expire = queries['expire']

        if not expire.isdecimal() or not 10 <= int(expire) <= 1800:
            raise BadRequestException()
        return int(expire)

    @staticmethod
    def _extract_content_type(queries):
        """ Content-Typeクエリパラメータを抽出＆チェックする関数
        条件：任意パラメータ、値の整合性はチェックしない

        :param queries: クエリパラメータのDictionary
        :return: ContentTypeの値
        """
        return queries['contenttype'] if 'contenttype' in queries else None

    @staticmethod
    def _extract_upload_path(paths):
        """ [バケット名、キー名のPrefix]パスパラメータを抽出＆チェックする関数
        条件：必須パラメータ
        　　：最小パス構成は、{バケット名}/urlとなり、キー名のPrefixは省略可能
        　　：キー名のPrefixは最大16階層まで指定可能

        :param paths: パスパラメータの値（先頭の/は含まれない）
        :return: バケット名、キー名のPrefix
        :raise: BadRequestException
        """
        if 'directory' not in paths:
            raise BadRequestException()
        directory = paths['directory']

        if len(directory.split('/')) < 2 or not directory.endswith('/url'):
            raise BadRequestException()
        bucket = directory[:directory.index('/')]

        key_prefix = directory[directory.index('/') + 1:directory.rindex('/') + 1]
        if key_prefix.count('/') > 16:
            raise BadRequestException()

        return bucket, key_prefix

    def __str__(self):
        return '{}/{}/{}/{}/{}'.format(
            self._method, self.expire, self.content_type, self.bucket, self.key)
