from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.models.charity_project import CharityProject
from app.schemas.donation import (DonationCreate,
                                  DonationCreateResponse,
                                  DonationDB)
from app.services.investment import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreateResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    projects_query = (
        select(CharityProject)
        .filter_by(fully_invested=False)
        .order_by(CharityProject.create_date)
    )
    projects_result = await session.execute(projects_query)
    sources = projects_result.scalars().all()
    invest_donations(new_donation, sources)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationCreateResponse],
    response_model_exclude_unset=True,
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
