from pubsub import pub

from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.call_failure_history_repository import (
    SyncFailureRepository,
)


def test_event(sync_session):
    # given
    def some_save_event(param) -> None:
        SyncFailureRepository(sync_session).save(fail_orm=param)

    pub.subscribe(some_save_event, "some_save_event")

    def call_event(param):
        send_message(topic_name="some_save_event", param=param)

    test_ref_id = 1
    test_ref_table = "kapt_area_infos"
    test_reason = "request failed"

    test_orm = CallFailureHistoryModel(
        ref_id=test_ref_id,
        ref_table=test_ref_table,
        reason=test_reason,
    )

    # when
    call_event(param=test_orm)

    # then
    repo = SyncFailureRepository(sync_session)
    get_orm = repo.find_by_id(1)

    assert get_orm.id == 1
    assert get_orm.ref_id == test_ref_id
    assert get_orm.ref_table == test_ref_table
    assert get_orm.reason == test_reason
