import datetime as dt
import os
from pathlib import Path

from app.config.properties.app_settings import AppSettings
from app.config.setup.logging_setup import initialize_root_logger, ConsoleHandleParams, StructuredConsoleHandleParams


class AppConfig:

    """
    AppConfig class creates an instance only if there is no instance created;
    otherwise return cls instance already created
    """

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AppConfig, cls).__new__(cls)
            cls._init()

        return cls.instance

    @classmethod
    def _init(cls):
        app_start_datetime_utc = dt.datetime.utcnow().isoformat()
        app_env = os.getenv('APP_ENV', 'dev').lower()
        deployed_flag = cls._convert_bool_os_env_var('DEPLOYED_FLAG', default_value=False)

        cls._init_logging(app_env, deployed_flag)

        cls.settings = AppSettings(
            app_start_datetime_utc=app_start_datetime_utc,
            env=app_env,
            deployed_flag=deployed_flag,
            root_dir=Path(os.path.abspath(__file__)).parents[3]
        )

    @staticmethod
    def _init_logging(app_env: str, deployed_flag: bool):
        log_settings = {'log_filter_params': {'app_env': app_env}}
        handler_params = (
            StructuredConsoleHandleParams(**log_settings) if deployed_flag else ConsoleHandleParams(**log_settings))

        initialize_root_logger(handler_params)

    @staticmethod
    def _convert_bool_os_env_var(env_var_name: str, default_value: bool) -> bool:
        env_var_value = os.getenv(env_var_name, default_value)

        if env_var_value and isinstance(env_var_value, str):
            result = True if env_var_value.lower() == 'true' else False
        else:
            result = env_var_value

        return result


# Global singleton instance of AppConfig
cfg = AppConfig()
