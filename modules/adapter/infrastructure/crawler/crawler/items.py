from pydantic import BaseModel, Field


class KaptAreaInfoItem(BaseModel):
    kapt_code: str = Field()
    name: str = Field()
    kapt_tarea: str | None = Field()
    kapt_marea: str | None = Field()
    kapt_mparea_60: str | None = Field()
    kapt_mparea_85: str | None = Field()
    kapt_mparea_135: str | None = Field()
    kapt_mparea_136: str | None = Field()
    priv_area: str | None = Field()
    bjd_code: str | None = Field()


class KaptLocationInfoItem(BaseModel):
    kapt_code: str = Field()
    name: str | None = Field()
    kaptd_wtimebus: str | None = Field()
    subway_line: str | None = Field()
    subway_station: str | None = Field()
    kaptd_wtimesub: str | None = Field()
    convenient_facility: str | None = Field()
    education_facility: str | None = Field()


class KakaoPlaceInfoItem(BaseModel):
    x_vl: float
    y_vl: float
    road_address: str | None
    jibun_address: str | None
    bld_name: str | None


class LegalDongCodeItem(BaseModel):
    region_cd: str | None
    sido_cd: str | None
    sgg_cd: str | None
    umd_cd: str | None
    ri_cd: str | None
    locatjumin_cd: str | None
    locatjijuk_cd: str | None
    locatadd_nm: str | None
    locat_order: str | None
    locat_rm: str | None
    locathigh_cd: str | None
    locallow_nm: str | None
    adpt_de: str | None


class GovtBldInputInfo(BaseModel):
    house_id: int
    kapt_code: str | None
    name: str | None
    origin_dong_address: str | None
    new_dong_address: str | None
    origin_bjd_code: str | None
    bun: str | None
    ji: str | None
    sigungu_code: str | None
    bjdong_code: str | None


class GovtBldTopInfoItem(BaseModel):
    house_id: int
    mgm_bldrgst_pk: str
    itg_bld_grade: str | None
    itg_bld_cert: str | None
    crtn_day: str | None
    na_bjdong_cd: str | None
    na_ugrnd_cd: str | None
    na_main_bun: float | None
    na_sub_bun: float | None
    plat_area: float | None
    arch_area: float | None
    bc_rat: float | None
    tot_area: float | None
    vl_rat_estm_tot_area: float | None
    vl_rat: float | None
    main_purps_cd: str | None
    main_purps_cd_nm: str | None
    etc_purps: str | None
    hhld_cnt: float | None
    fmly_cnt: float | None
    main_bld_cnt: float | None
    atch_bld_cnt: float | None
    atch_bld_area: float | None
    tot_pkng_cnt: float | None
    indr_mech_utcnt: float | None
    indr_mech_area: float | None
    oudr_mech_utcnt: float | None
    oudr_mech_area: float | None
    indr_auto_utcnt: float | None
    indr_auto_area: float | None
    oudr_auto_utcnt: float | None
    oudr_auto_area: float | None
    pms_day: str | None
    stcns_day: str | None
    use_apr_day: str | None
    pmsno_year: str | None
    pmsno_kik_cd: str | None
    pmsno_kik_cd_nm: str | None
    pmsno_gb_cd: str | None
    pmsno_gb_cd_nm: str | None
    ho_cnt: float | None
    engr_grade: str | None
    engr_rat: float | None
    engr_epi: float | None
    gn_bld_grade: str | None
    gn_bld_cert: float | None
    rnum: float | None
    plat_plc: str | None
    sigungu_cd: str | None
    bjdong_cd: str | None
    plat_gb_cd: str | None
    bun: str | None
    ji: str | None
    regstr_gb_cd: str | None
    regstr_gb_cd_nm: str | None
    regstr_kind_cd: str | None
    regstr_kind_cd_nm: str | None
    new_old_regstr_gb_cd: str | None
    new_old_regstr_gb_cd_nm: str | None
    new_plat_plc: str | None
    bld_nm: str | None
    splot_nm: str | None
    block: str | None
    lot: str | None
    bylot_cnt: float | None
    na_road_cd: str | None


class GovtBldMidInfoItem(BaseModel):
    house_id: int
    mgm_bldrgst_pk: str
    main_purps_cd_nm: str | None
    etc_purps: str | None
    roof_cd: str | None
    roof_cd_nm: str | None
    etc_roof: str | None
    hhld_cnt: float | None
    fmly_cnt: float | None
    heit: float | None
    grnd_flr_cnt: float | None
    ugrnd_flr_cnt: float | None
    ride_use_elvt_cnt: float | None
    emgen_use_elvt_cnt: float | None
    atch_bld_cnt: float | None
    atch_bld_area: float | None
    tot_dong_tot_area: float | None
    indr_mech_utcnt: float | None
    indr_mech_area: float | None
    oudr_mech_utcnt: float | None
    oudr_mech_area: float | None
    indr_auto_utcnt: float | None
    indr_auto_area: float | None
    oudr_auto_utcnt: float | None
    oudr_auto_area: float | None
    pms_day: str | None
    stcns_day: str | None
    use_apr_day: str | None
    pmsno_year: str | None
    pmsno_kik_cd: str | None
    pmsno_kik_cd_nm: str | None
    pmsno_gb_cd: str | None
    pmsno_gb_cd_nm: str | None
    ho_cnt: float | None
    engr_grade: str | None
    engr_rat: float | None
    engr_epi: float | None
    gn_bld_grade: str | None
    gn_bld_cert: float | None
    itg_bld_grade: str | None
    itg_bld_cert: float | None
    crtn_day: str | None
    rnum: float | None
    plat_plc: str | None
    sigungu_cd: str | None
    bjdong_cd: str | None
    plat_gb_cd: str | None
    bun: str | None
    ji: str | None
    regstr_gb_cd: str | None
    regstr_gb_cd_nm: str | None
    regstr_kind_cd: str | None
    regstr_kind_cd_nm: str | None
    new_plat_plc: str | None
    bld_nm: str | None
    splot_nm: str | None
    block: str | None
    lot: str | None
    bylot_cnt: float | None
    na_road_cd: str | None
    na_bjdong_cd: str | None
    na_ugrnd_cd: str | None
    na_main_bun: float | None
    na_sub_bun: float | None
    dong_nm: str | None
    main_atch_gb_cd: str | None
    main_atch_gb_cd_nm: str | None
    plat_area: float | None
    arch_area: float | None
    bc_rat: float | None
    tot_area: float | None
    vl_rat_estm_tot_area: float | None
    vl_rat: float | None
    strct_cd: str | None
    strct_cd_nm: str | None
    etc_strct: str | None
    main_purps_cd: str | None
    rserthqk_dsgn_apply_yn: str | None
    rserthqk_ablty: str | None


class GovtBldAreaInfoItem(BaseModel):
    house_id: int
    mgm_bldrgst_pk: str
    regstr_gb_cd: str | None
    regstr_gb_cd_nm: str | None
    regstr_kind_cd: str | None
    regstr_kind_cd_nm: str | None
    new_plat_plc: str | None
    bld_nm: str | None
    splot_nm: str | None
    block: str | None
    lot: str | None
    na_road_cd: str | None
    na_bjdong_cd: str | None
    na_ugrnd_cd: str | None
    na_main_bun: float | None
    na_sub_bun: float | None
    dong_nm: str | None
    ho_nm: str | None
    flr_gb_cd: str | None
    flr_gb_cd_nm: str | None
    flr_no: float | None
    flr_no_nm: str | None
    expos_pubuse_gb_cd: str | None
    expos_pubuse_gb_cd_nm: str | None
    main_atch_gb_cd: str | None
    main_atch_gb_cd_nm: str | None
    strct_cd: str | None
    strct_cd_nm: str | None
    etc_strct: str | None
    main_purps_cd: str | None
    main_purps_cd_nm: str | None
    etc_purps: str | None
    area: float | None
    crtn_day: str | None
    rnum: float | None
    plat_plc: str | None
    sigungu_cd: str | None
    bjdong_cd: str | None
    plat_gb_cd: str | None
    bun: str | None
    ji: str | None


class GovtAptDealInfoItem(BaseModel):
    deal_amount: int | None
    build_year: str | None
    deal_year: str | None
    road_name: str | None
    road_name_bonbun: str | None
    road_name_bubun: str | None
    road_name_sigungu_cd: str | None
    road_name_seq: str | None
    road_name_basement_cd: str | None
    road_name_cd: str | None
    dong: str | None
    bonbun_cd: str | None
    bubun_cd: str | None
    sigungu_cd: str | None
    eubmyundong_cd: str | None
    land_cd: str | None
    apt_name: str | None
    deal_month: str | None
    deal_day: str | None
    serial_no: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None


class GovtAptRentInfoItem(BaseModel):
    build_year: str | None
    deal_year: str | None
    dong: str | None
    deposit: int | None
    apt_name: str | None
    deal_month: str | None
    deal_day: str | None
    monthly_amount: int | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None


class GovtOfctlDealInfoItem(BaseModel):
    deal_amount: int | None
    deal_year: str | None
    ofctl_name: str | None
    dong: str | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None


class GovtOfctlRentInfoItem(BaseModel):
    deal_year: str | None
    ofctl_name: str | None
    dong: str | None
    deposit: int | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    monthly_amount: int | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None


class GovtRightLotOutInfoItem(BaseModel):
    deal_amount: int | None
    classification_owner_ship: str | None
    deal_year: str | None
    name: str | None
    dong: str | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
