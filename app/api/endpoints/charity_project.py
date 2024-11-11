from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_exists,
    check_project_name_duplicate,
    check_project_not_closed,
    check_project_not_invested,
    check_required_amount_not_less_than_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await invest_donations(session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_project_not_closed(charity_project)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session,
                                           project_id=project_id)
    if obj_in.full_amount is not None:
        await check_required_amount_not_less_than_invested(charity_project,
                                                           obj_in.full_amount)
        if obj_in.full_amount == charity_project.invested_amount:
            charity_project.close_date = datetime.now()
    updated_project = await charity_project_crud.update(charity_project,
                                                        obj_in, session)
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_project_not_closed(charity_project)
    await check_project_not_invested(charity_project)
    deleted_project = await charity_project_crud.remove(
        charity_project, session)
    await session.commit()
    return deleted_project
