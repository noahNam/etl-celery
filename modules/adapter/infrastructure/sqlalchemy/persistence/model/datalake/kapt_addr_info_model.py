# from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, CHAR
# from sqlalchemy import Column
#
# from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
#     TimestampMixin,
# )
# from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
#
#
# class KaptAddrInfoModel(datalake_base, TimestampMixin):
#     __tablename__ = "kapt_addr_infos"
#
#     house_id = Column(
#         BIGINT,
#         nullable=False,
#         primary_key=True,
#     )
#     addr_code = Column(CHAR(10), nullable=True)
#     jibun = Column(VARCHAR(10), nullable=True)
