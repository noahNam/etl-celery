from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int
    email: str | None
    is_required_agree_terms: bool
    join_date: str
    is_active: bool
    is_out: bool
    number_ticket: int
