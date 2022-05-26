from datetime import datetime

from pydantic import BaseModel


class CallFailureHistoryEntity(BaseModel):
    id: int
    ref_id: int
    ref_table: str | None
    reason: str | None
    is_solved: bool
    created_at: datetime
    updated_at: datetime
