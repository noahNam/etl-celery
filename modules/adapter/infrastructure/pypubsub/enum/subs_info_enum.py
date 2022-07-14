from enum import Enum


class SubsInfoTopicEnum(Enum):
    BULK_SAVE_SUBSCRIPTION_INFOS = "bulk_save_subscription_infos"
    UPDATE_TO_NEW_SCHEMA = "update_to_new_schema"
    SAVE_ALL = "save_all"
    FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH = "find_subscription_infos_by_year_month"
