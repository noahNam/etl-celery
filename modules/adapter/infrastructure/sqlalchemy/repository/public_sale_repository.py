from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)


class PublicSaleRepository:
    def save_all(self, models: list[PublicSaleModel]) -> None:
        pass
