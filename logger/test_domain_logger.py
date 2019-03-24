from unittest import TestCase
from logger.domain_logger import DomainLogger
from logging import getLogger, Formatter, StreamHandler, DEBUG


class TestDomainLogger(TestCase):
    """ logger.domain_logger.DomainLoggerのテストクラス
    """
    def setUp(self):
        pass

    def test_logger_case_new_handler(self):
        """ ログ出力の正常系テスト
        条件：新規のHandlerを作成するように、ロガー名を指定
        結果：標準出力のチェックが難しいため、目視確認
        """
        logger = DomainLogger.get_logger(name='new', level='DEBUG')

        logger.debug('Hello, debug log.')
        logger.debug('Hello, debug log.', 'D0001')
        logger.info('Hello, info log.')
        logger.info('Hello, info log.', 'I0001')
        logger.warning('Hello, warning log.', 'W0001')
        logger.error('Hello, error log.', 'E0001')

        try:
            raise ValueError('Invalid value.')
        except ValueError as e:
            logger.exception(e, 'E0002')

    def test_logger_case_existing_handler(self):
        """ ログ出力の正常系テスト
        条件：既存のHandlerを使用するように、ロガー名を指定
        結果：標準出力のチェックが難しいため、目視確認
        """
        logger = getLogger('existing')
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.addHandler(handler)

        logger = DomainLogger.get_logger(name='existing', level='DEBUG')

        logger.debug('Hello, debug log.')
        logger.debug('Hello, debug log.', 'D0001')
        logger.info('Hello, info log.')
        logger.info('Hello, info log.', 'I0001')
        logger.warning('Hello, warning log.', 'W0001')
        logger.error('Hello, error log.', 'E0001')

        try:
            raise ValueError('Invalid value.')
        except ValueError as e:
            logger.exception(e, 'E0002')
