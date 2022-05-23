from pydantic import BaseModel


class MessageDto(BaseModel):
    msg: dict