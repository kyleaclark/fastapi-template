from pydantic import BaseModel


class ZenGetResModel(BaseModel):
    message: str
