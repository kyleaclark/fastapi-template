from dataclasses import dataclass
from pathlib import PosixPath, WindowsPath
from typing import Union


@dataclass
class AppSettings:
    app_start_datetime_utc: str
    env: str
    deployed_flag: bool
    root_dir: Union[PosixPath, WindowsPath]
