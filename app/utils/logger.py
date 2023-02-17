import loguru

from app.config import Config
from utils import SingletonDecorator


@SingletonDecorator
class Logger:
    def __init__(self, name="log", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"):
        """
        初始化日志记录器。

        Args:
            log_file_path (str): 日志文件路径。
            level (str): 日志记录器的日志级别，默认为 INFO。
            format (str): 日志消息格式，默认为 "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"。
        """
        self.log_file_path = Config().log_name()

        self.logger = loguru.logger
        self.logger.remove()
        self.logger.add(self.log_file_path, rotation="10 MB", level=level, format=format)
        print(self.log_file_path)

    def info(self, message, **kwargs):
        """
        记录 INFO 级别的日志消息。

        Args:
            message (str): 日志消息。
            **kwargs: 附加到日志消息的键值对上下文信息。
        """
        self.logger.info(message, **kwargs)

    def debug(self, message, **kwargs):
        """
        记录 DEBUG 级别的日志消息。

        Args:
            message (str): 日志消息。
            **kwargs: 附加到日志消息的键值对上下文信息。
        """
        self.logger.debug(message, **kwargs)

    def warning(self, message, **kwargs):
        """
        记录 WARNING 级别的日志消息。

        Args:
            message (str): 日志消息。
            **kwargs: 附加到日志消息的键值对上下文信息。
        """
        self.logger.warning(message, **kwargs)

    def error(self, message, **kwargs):
        """
        记录 ERROR 级别的日志消息。

        Args:
            message (str): 日志消息。
            **kwargs: 附加到日志消息的键值对上下文信息。
        """
        self.logger.error(message, **kwargs)

    def critical(self, message, **kwargs):
        """
        记录 CRITICAL 级别的日志消息。

        Args:
            message (str): 日志消息。
            **kwargs: 附加到日志消息的键值对上下文信息。
        """
        self.logger.critical(message, **kwargs)
