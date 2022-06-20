from sqlalchemy import Column, String, BigInteger, Integer, Numeric, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GovtBldAreaInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_bld_area_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    mgm_bldrgst_pk = Column(String(33), nullable=True, index=True, unique=True)
    regstr_gb_cd = Column(String(1), nullable=True)
    regstr_gb_cd_nm = Column(String(100), nullable=True)
    regstr_kind_cd = Column(String(1), nullable=True)
    regstr_kind_cd_nm = Column(String(100), nullable=True)
    new_plat_plc = Column(String(200), nullable=True)
    bld_nm = Column(String(100), nullable=True)
    splot_nm = Column(String(200), nullable=True)
    block = Column(String(20), nullable=True)
    lot = Column(String(20), nullable=True)
    na_road_cd = Column(String(12), nullable=True)
    na_bjdong_cd = Column(String(5), nullable=True)
    na_ugrnd_cd = Column(String(1), nullable=True)
    na_main_bun = Column(Numeric(5), nullable=True)
    na_sub_bun = Column(Numeric(5), nullable=True)
    dong_nm = Column(String(100), nullable=True)
    ho_nm = Column(String(100), nullable=True)
    flr_gb_cd = Column(String(2), nullable=True)
    flr_gb_cd_nm = Column(String(100), nullable=True)
    flr_no = Column(Numeric(4), nullable=True)
    flr_no_nm = Column(String(100), nullable=True)
    expos_pubuse_gb_cd = Column(String(1), nullable=True)
    expos_pubuse_gb_cd_nm = Column(String(100), nullable=True)
    main_atch_gb_cd = Column(String(1), nullable=True)
    main_atch_gb_cd_nm = Column(String(100), nullable=True)
    strct_cd = Column(String(1), nullable=True)
    strct_cd_nm = Column(String(100), nullable=True)
    etc_strct = Column(String(500), nullable=True)
    main_purps_cd = Column(String(5), nullable=True)
    main_purps_cd_nm = Column(String(100), nullable=True)
    etc_purps = Column(String(500), nullable=True)
    area = Column(Numeric(19, 9), nullable=True)
    crtn_day = Column(String(8), nullable=True)
    rnum = Column(Integer, nullable=True)
    plat_plc = Column(String(200), nullable=True)
    sigungu_cd = Column(String(5), nullable=True, index=True)
    bjdong_cd = Column(String(5), nullable=True, index=True)
    plat_gb_cd = Column(String(1), nullable=True)
    bun = Column(String(4), nullable=True)
    ji = Column(String(4), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_govt_bld_area_info_entity(self) -> GovtBldAreaInfoEntity:
        return GovtBldAreaInfoEntity(
            house_id=self.house_id,
            area=self.area,
            bld_nm=self.bld_nm,
            dong_nm=self.dong_nm,
            ho_nm=self.ho_nm,
            flr_no_nm=self.flr_no_nm,
            main_atch_gb_cd=self.main_atch_gb_cd,
            main_atch_gb_cd_nm=self.main_atch_gb_cd_nm,
            etc_purps=self.etc_purps,
            expos_pubuse_gb_cd_nm=self.expos_pubuse_gb_cd_nm,
            rnum=self.rnum,
        )
