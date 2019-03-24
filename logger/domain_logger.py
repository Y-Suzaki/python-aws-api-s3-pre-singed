from logging import getLogger, Formatter, StreamHandler
import time


class DomainLogger:
    """ コンソール出力用のログを扱うクラス
    """
    @staticmethod
    def get_logger(name='DomainLogger', level='INFO'):
        """ ロガーを取得
        __init__ではなく、本関数でオブジェクトを取得すること
        """
        return DomainLogger(name, level)

    @staticmethod
    def _get_formatter():
        """ ログフォーマットを取得
        日時はUTC表記にすること
        """
        formatter = Formatter('%(levelname)s %(error_code)s %(asctime)s %(message)s', '%Y-%m-%dT%H:%M:%SZ')
        formatter.converter = time.gmtime
        return formatter

    def __init__(self, name, level):
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        formatter = DomainLogger._get_formatter()

        if self.logger.handlers:
            for handler in self.logger.handlers:
                handler.setFormatter(formatter)
        else:
            handler = StreamHandler()
            handler.setLevel(level)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, message, error_code='-'):
        self.logger.debug(message, extra={'error_code': error_code})

    def info(self, message, error_code='-'):
        self.logger.info(message, extra={'error_code': error_code})

    def warning(self, message, error_code):
        self.logger.warning(message, extra={'error_code': error_code})

    def error(self, message, error_code):
        self.logger.error(message, extra={'error_code': error_code})

    def exception(self, message, error_code):
        self.logger.exception(message, extra={'error_code': error_code})
