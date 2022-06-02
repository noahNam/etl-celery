from uuid import uuid4

from core.domain.kapt.interface.kapt_repository import KaptRepository
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import (
    KaptBasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    AsyncKaptRepository,
    SyncKaptRepository,
)


async def test_find_by_id(async_session):
    repo: KaptRepository = AsyncKaptRepository(async_session)
    house_id = 1
    name = "test_apt"
    test_kapt_input = KaptBasicInfoModel(
        house_id=house_id,
        kapt_code="EXAMPLE_KAPT",
        name=name,
        place_id=10,
    )

    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    async with async_session() as session:
        session.add(test_kapt_input)
        await session.commit()
    get_kapt: KaptOpenApiInputEntity | None = await repo.find_by_id(house_id=house_id)

    SessionContextManager.reset_context(context=context)
    assert isinstance(get_kapt, KaptOpenApiInputEntity)
    assert house_id == get_kapt.house_id
    assert name == get_kapt.name


async def test_find_all(async_session):
    repo: KaptRepository = AsyncKaptRepository(async_session)
    house_ids = [1, 2]
    names = ["test_apt_1", "test_api_2"]
    test_kapt_1 = KaptBasicInfoModel(
        house_id=house_ids[0],
        kapt_code="EXAMPLE_KAPT_1",
        name=names[0],
        place_id=10,
    )
    test_kapt_2 = KaptBasicInfoModel(
        house_id=house_ids[1],
        kapt_code="EXAMPLE_KAPT_2",
        name=names[1],
        place_id=20,
    )

    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    async with async_session() as session:
        session.add_all([test_kapt_1, test_kapt_2])
        await session.commit()
    get_kapts: list[KaptOpenApiInputEntity] | None = await repo.find_all()

    SessionContextManager.reset_context(context=context)
    for kapt, house_id, name in zip(get_kapts, house_ids, names):
        assert isinstance(kapt, KaptOpenApiInputEntity)
        assert kapt.house_id == house_id
        assert kapt.name == name


def test_sync_find_by_id(sync_session):
    repo: KaptRepository = SyncKaptRepository(sync_session)
    house_id = 1
    name = "test_apt"
    test_kapt_input = KaptBasicInfoModel(
        house_id=house_id,
        kapt_code="EXAMPLE_KAPT",
        name=name,
        place_id=10,
    )

    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    with sync_session() as session:
        session.add(test_kapt_input)
        session.commit()
    get_kapt: KaptOpenApiInputEntity | None = repo.find_by_id(house_id=house_id)

    SessionContextManager.reset_context(context=context)
    assert isinstance(get_kapt, KaptOpenApiInputEntity)
    assert house_id == get_kapt.house_id
    assert name == get_kapt.name


def test_sync_find_all(sync_session):
    repo: KaptRepository = SyncKaptRepository(sync_session)
    house_ids = [1, 2]
    names = ["test_apt_1", "test_api_2"]
    test_kapt_1 = KaptBasicInfoModel(
        house_id=house_ids[0],
        kapt_code="EXAMPLE_KAPT_1",
        name=names[0],
        place_id=10,
    )
    test_kapt_2 = KaptBasicInfoModel(
        house_id=house_ids[1],
        kapt_code="EXAMPLE_KAPT_2",
        name=names[1],
        place_id=20,
    )

    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    with sync_session() as session:
        session.add_all([test_kapt_1, test_kapt_2])
        session.commit()
        get_kapts: list[KaptOpenApiInputEntity] | None = repo.find_all()

    SessionContextManager.reset_context(context=context)
    for kapt, house_id, name in zip(get_kapts, house_ids, names):
        assert isinstance(kapt, KaptOpenApiInputEntity)
        assert kapt.house_id == house_id
        assert kapt.name == name


def test_exists_by_kapt_code(sync_session):
    repo: KaptRepository = SyncKaptRepository(sync_session)
    house_ids: list[str] = ["abcde123", "qwert456", "no_saved"]
    names = ["test_apt_1", "test_api_2", "test_api_3"]

    test_kapt_1 = KaptAreaInfoModel(
        kapt_code=house_ids[0],
        name=names[0],
    )
    test_kapt_2 = KaptLocationInfoModel(
        kapt_code=house_ids[1],
        name=names[1],
    )
    test_kapt_3 = KaptLocationInfoModel(
        kapt_code=house_ids[2],
        name=names[2],
    )

    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    with sync_session() as session:
        session.add_all([test_kapt_1, test_kapt_2])
        session.commit()

        result_kapt_1 = repo.exists_by_kapt_code(kapt_orm=test_kapt_1)
        result_kapt_3 = repo.exists_by_kapt_code(kapt_orm=test_kapt_3)

    SessionContextManager.reset_context(context=context)

    assert result_kapt_1 is True
    assert result_kapt_3 is False
