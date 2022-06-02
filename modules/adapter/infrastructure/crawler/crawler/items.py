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
