from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageDto(BaseModel):
    created_at: datetime
    uuid: UUID
    msg: dict

    def to_dict(self):
        return {
            "created_at": self.created_at.replace(microsecond=0).isoformat(),
            "uuid": str(self.uuid),
            "msg": self.msg,
        }