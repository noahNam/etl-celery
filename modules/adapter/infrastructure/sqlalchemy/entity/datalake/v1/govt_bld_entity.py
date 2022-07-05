from pydantic import BaseModel


class GovtBldTopInfoEntity(BaseModel):
    house_id: int
    bjdong_cd: str | None
    sigungu_cd: str | None
    bun: str | None
    ji: str | None
    bc_rat: float | None
    vl_rat: float | None
    update_needed: bool


class GovtBldMiddleInfoEntity(BaseModel):
    house_id: int
    dong_id: int | None  # schema model 에는 없지만 ETL시 관계 참조용 변수로 선언
    dong_nm: str | None
    hhld_cnt: int | None
    grnd_flr_cnt: int | None
    update_needed: bool


class GovtBldAreaInfoEntity(BaseModel):
    house_id: int
    dong_id: int | None  # schema model 에는 없지만 ETL시 관계 참조용 변수로 선언
    area: float | None
    bld_nm: str | None
    dong_nm: str | None
    ho_nm: str | None
    flr_no_nm: str | None
    main_atch_gb_cd: str | None
    main_atch_gb_cd_nm: str | None
    main_purps_cd: str | None
    etc_purps: str | None
    expos_pubuse_gb_cd_nm: str | None
    rnum: int | None
    update_needed: bool
