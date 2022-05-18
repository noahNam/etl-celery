from uuid import uuid4

from core.domain.kapt.interface.kapt_repository import KaptRepository
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import (
    KaptBasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    AsyncKaptRepository,
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
