from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Numeric,
    SmallInteger,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldMiddleInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GovtBldMiddleInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_bld_middle_infos"

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
    main_purps_cd_nm = Column(String(100), nullable=True)
    etc_purps = Column(String(500), nullable=True)
    roof_cd = Column(String(2), nullable=True)
    roof_cd_nm = Column(String(100), nullable=True)
    etc_roof = Column(String(500), nullable=True)
    hhld_cnt = Column(SmallInteger, nullable=True)
    fmly_cnt = Column(SmallInteger, nullable=True)
    heit = Column(Numeric(19, 9), nullable=True)
    grnd_flr_cnt = Column(SmallInteger, nullable=True)
    ugrnd_flr_cnt = Column(Numeric(5), nullable=True)
    ride_use_elvt_cnt = Column(Numeric(5), nullable=True)
    emgen_use_elvt_cnt = Column(Numeric(5), nullable=True)
    atch_bld_cnt = Column(Numeric(5), nullable=True)
    atch_bld_area = Column(Numeric(19, 9), nullable=True)
    tot_dong_tot_area = Column(Numeric(19, 9), nullable=True)
    indr_mech_utcnt = Column(Numeric(6), nullable=True)
    indr_mech_area = Column(Numeric(19, 9), nullable=True)
    oudr_mech_utcnt = Column(Numeric(6), nullable=True)
    oudr_mech_area = Column(Numeric(19, 9), nullable=True)
    indr_auto_utcnt = Column(Numeric(6), nullable=True)
    indr_auto_area = Column(Numeric(19, 9), nullable=True)
    oudr_auto_utcnt = Column(Numeric(6), nullable=True)
    oudr_auto_area = Column(Numeric(19, 9), nullable=True)
    pms_day = Column(String(8), nullable=True)
    stcns_day = Column(String(8), nullable=True)
    use_apr_day = Column(String(8), nullable=True)
    pmsno_year = Column(String(4), nullable=True)
    pmsno_kik_cd = Column(String(7), nullable=True)
    pmsno_kik_cd_nm = Column(String(100), nullable=True)
    pmsno_gb_cd = Column(String(4), nullable=True)
    pmsno_gb_cd_nm = Column(String(100), nullable=True)
    ho_cnt = Column(Numeric(5), nullable=True)
    engr_grade = Column(String(4), nullable=True)
    engr_rat = Column(Numeric(19, 9), nullable=True)
    engr_epi = Column(Numeric(5), nullable=True)
    gn_bld_grade = Column(String(1), nullable=True)
    gn_bld_cert = Column(Numeric(5), nullable=True)
    itg_bld_grade = Column(String(1), nullable=True)
    itg_bld_cert = Column(Numeric(5), nullable=True)
    crtn_day = Column(String(8), nullable=True)
    rnum = Column(Numeric(8), nullable=True)
    plat_plc = Column(String(200), nullable=True)
    sigungu_cd = Column(String(5), nullable=True, index=True)
    bjdong_cd = Column(String(5), nullable=True, index=True)
    plat_gb_cd = Column(String(1), nullable=True)
    bun = Column(String(4), nullable=True)
    ji = Column(String(4), nullable=True)
    regstr_gb_cd = Column(String(1), nullable=True)
    regstr_gb_cd_nm = Column(String(100), nullable=True)
    regstr_kind_cd = Column(String(1), nullable=True)
    regstr_kind_cd_nm = Column(String(100), nullable=True)
    new_plat_plc = Column(String(200), nullable=True)
    bld_nm = Column(String(100), nullable=True)
    splot_nm = Column(String(200), nullable=True)
    block = Column(String(20), nullable=True)
    lot = Column(String(20), nullable=True)
    bylot_cnt = Column(Numeric(5), nullable=True)
    na_road_cd = Column(String(12), nullable=True)
    na_bjdong_cd = Column(String(5), nullable=True)
    na_ugrnd_cd = Column(String(1), nullable=True)
    na_main_bun = Column(Numeric(5), nullable=True)
    na_sub_bun = Column(Numeric(5), nullable=True)
    dong_nm = Column(String(100), nullable=True)
    main_atch_gb_cd = Column(String(1), nullable=True)
    main_atch_gb_cd_nm = Column(String(100), nullable=True)
    plat_area = Column(Numeric(19, 9), nullable=True)
    arch_area = Column(Numeric(19, 9), nullable=True)
    bc_rat = Column(Numeric(19, 9), nullable=True)
    tot_area = Column(Numeric(19, 9), nullable=True)
    vl_rat_estm_tot_area = Column(Numeric(19, 9), nullable=True)
    vl_rat = Column(Numeric(19, 9), nullable=True)
    strct_cd = Column(String(1), nullable=True)
    strct_cd_nm = Column(String(100), nullable=True)
    etc_strct = Column(String(500), nullable=True)
    main_purps_cd = Column(String(5), nullable=True)
    rserthqk_dsgn_apply_yn = Column(String(1), nullable=True)
    rserthqk_ablty = Column(String(200), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=False)

    def to_govt_bld_top_info_entity(self) -> GovtBldMiddleInfoEntity:
        return GovtBldMiddleInfoEntity(
            house_id=self.house_id,
            dong_nm=self.dong_nm,
            hhld_cnt=self.hhld_cnt,
            grnd_flr_cnt=self.grnd_flr_cnt,
            update_needed=self.update_needed
        )
