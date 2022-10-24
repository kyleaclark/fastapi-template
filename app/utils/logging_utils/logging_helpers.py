from dataclasses import asdict, dataclass, is_dataclass
from typing import Union


def generate_log_extra(metadata: Union[dict, dataclass]) -> dict:
    if is_dataclass(metadata):
        metadata = asdict(metadata)

    result = {'metadata': metadata}

    return result
