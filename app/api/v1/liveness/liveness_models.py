from pydantic import BaseModel


class LivenessGetResModel(BaseModel):
    appStartDatetimeUTC: str
    environment: str
    deployedFlag: bool
    requestDatetimeUTC: str
