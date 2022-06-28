from pydantic import BaseModel


class PublicDtUniqueEntity(BaseModel):
    id: int
    public_sale_id: int
    area_type: str | None
    private_area: float
