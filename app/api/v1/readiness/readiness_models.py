from pydantic import BaseModel


class ReadinessGetResModel(BaseModel):
    appStartDatetimeUTC: str
    environment: str
    deployedFlag: bool
    requestDatetimeUTC: str
