from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
        project_id: int = None,
) -> None:
    project = await charity_project_crud.get_project_by_name(
        project_name, session)
    if project and (project_id is None or project.id != project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_required_amount_not_less_than_invested(
        project: CharityProject,
        new_full_amount: int,
) -> None:
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Требуемая сумма ({new_full_amount}) не может быть меньше '
                f'внесённой суммы ({project.invested_amount})!'
            )
        )


async def check_project_not_invested(
        project: CharityProject,
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить проект, в который уже внесены средства!'
        )


async def check_project_not_closed(
        project: CharityProject,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить закрытый проект!'
        )
