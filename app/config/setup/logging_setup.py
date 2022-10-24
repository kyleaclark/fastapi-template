import logging
from dataclasses import dataclass, field
from typing import Union

from pythonjsonlogger.jsonlogger import JsonFormatter

from app.utils.logging_utils.logging_helpers import generate_log_extra


# LOG FORMATS
#############

CONDENSED_LOG_FORMAT = '%(asctime)s %(appEnv)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s'

EXPANDED_LOG_FORMAT = (
    '%(asctime)s %(appEnv)s %(created)f %(exc_info)s %(filename)s %(funcName)s '
    '%(levelname)s %(lineno)d %(module)s %(message)s %(metadata)s %(pathname)s '
    '%(process)s %(processName)s %(relativeCreated)d %(thread)s %(threadName)s'
)


# LOG HANDLER CLASS HELPERS
###########################

class ContextLogFilter(logging.Filter):

    def __init__(self, app_env: str):
        self._app_env = app_env
        super().__init__()

    def filter(self, record):
        record.appEnv = self._app_env
        return True


@dataclass
class ConsoleHandleParams:
    enabled: bool = True
    log_level: int = logging.DEBUG  # logging.NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
    format: str = CONDENSED_LOG_FORMAT
    format_args: dict = field(default_factory=lambda: {})
    formatter: type(logging.Formatter) = logging.Formatter
    log_filter: type(logging.Filter) = ContextLogFilter
    log_filter_params: dict = field(default_factory=lambda: {})


@dataclass
class StructuredConsoleHandleParams(ConsoleHandleParams):
    log_level: int = logging.INFO
    format: str = EXPANDED_LOG_FORMAT
    formatter: type(logging.Formatter) = JsonFormatter


# LOGGING CONFIGURATION
#######################

def initialize_root_logger(console_handle_params: Union[ConsoleHandleParams, StructuredConsoleHandleParams]):
    """Initialize settings for root logger"""

    root_logger = logging.getLogger()

    # Remove any handlers that may exist on the root logger to explicitly control which handlers are applied
    if root_logger.propagate and root_logger.hasHandlers():
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Set lowest log level as a threshold for all root logger handlers
    root_logger.setLevel(logging.NOTSET)

    # Add console (stream) handler
    if console_handle_params.enabled:
        root_logger.addHandler(create_console_handler(console_handle_params))

    # Root logger initialized log output
    metadata = {'console_log_level': logging._levelToName[console_handle_params.log_level]}
    logger = logging.getLogger(__name__)
    logger.info('Initialized root logger', extra=generate_log_extra(metadata))


def create_console_handler(
        handler_params: Union[ConsoleHandleParams, StructuredConsoleHandleParams]) -> logging.StreamHandler:
    """Create a console handler (StreamHandler) from given param settings"""

    handler = logging.StreamHandler()
    handler.setLevel(handler_params.log_level)
    handler.setFormatter(handler_params.formatter(fmt=handler_params.format, **handler_params.format_args))

    if handler_params.log_filter and handler_params.log_filter_params:
        log_filter = handler_params.log_filter(**handler_params.log_filter_params)
        handler.addFilter(log_filter)

    return handler
