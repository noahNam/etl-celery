from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    DongInfoEntity,
    TypeInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.type_info_model import (
    TypeInfoModel,
)


class TransformDongTypeInfos:
    def start_etl(
        self,
        target_list: list[DongInfoEntity | TypeInfoEntity],
    ) -> list[DongInfoModel | TypeInfoModel] | None:
        if not target_list:
            return None

        if isinstance(target_list[0], DongInfoEntity):
            return self._etl_dong_infos(dong_infos=target_list)
        elif isinstance(target_list[0], TypeInfoEntity):
            return self._etl_type_infos(type_infos=target_list)

    def _etl_dong_infos(
        self,
        dong_infos: list[DongInfoEntity],
    ) -> list[DongInfoModel]:

        result = list()
        for dong_info in dong_infos:
            result.append(
                DongInfoModel(
                    id=dong_info.id,
                    private_sale_id=dong_info.house_id,
                    name=dong_info.name,
                    hhld_cnt=dong_info.hhld_cnt,
                    grnd_flr_cnt=dong_info.grnd_flr_cnt,
                    update_needed=dong_info.update_needed,
                )
            )
        return result

    def _etl_type_infos(
        self,
        type_infos: list[TypeInfoEntity],
    ) -> list[TypeInfoModel]:

        result = list()
        for type_info in type_infos:
            result.append(
                TypeInfoModel(
                    id=type_info.id,
                    dong_id=type_info.dong_id,
                    private_area=type_info.private_area,
                    supply_area=type_info.supply_area,
                    update_needed=type_info.update_needed,
                )
            )
        return result

    def filter_by_fk(
        self,
        type_infos: list[TypeInfoEntity] | None,
        filter_list: list[DongInfoEntity] | None,
    ) -> list[TypeInfoEntity] | None:
        if not type_infos or not filter_list:
            return None



