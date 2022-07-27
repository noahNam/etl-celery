from pydantic import BaseModel


class PublicSalePhotoEntity(BaseModel):
    id: int
    subs_id: int
    file_name: str
    path: str
    extension: str
    is_thumbnail: bool
    seq: int
    is_available: bool


class PublicSaleDtPhotoEntity(BaseModel):
    id: int
    subs_id: int
    file_name: str
    path: str
    extension: str
    is_available: bool
    update_needed: bool
