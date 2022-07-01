from pydantic import BaseModel


class KaptAddrInfoEntity(BaseModel):
    house_id: int
    addr_code: str | None
    jibun: str | None
