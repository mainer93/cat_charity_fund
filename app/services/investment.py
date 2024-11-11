from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_donations(session: AsyncSession) -> None:
    projects_query = (
        select(CharityProject)
        .filter_by(fully_invested=False)
        .order_by(CharityProject.create_date)
    )
    donations_query = (
        select(Donation)
        .filter_by(fully_invested=False)
        .order_by(Donation.create_date)
    )
    projects_result = await session.execute(projects_query)
    donations_result = await session.execute(donations_query)
    projects = projects_result.scalars().all()
    donations = donations_result.scalars().all()
    for project in projects:
        required_project_amount = (
            project.full_amount - project.invested_amount
        )
        if required_project_amount <= 0:
            continue
        for donation in donations:
            available_donation_amount = (
                donation.full_amount - donation.invested_amount
            )
            if available_donation_amount <= 0:
                continue
            investment_amount = min(
                available_donation_amount,
                required_project_amount
            )
            update_investment(
                project,
                donation,
                investment_amount
            )
            required_project_amount -= investment_amount
            if project.fully_invested:
                break
    await session.commit()


def update_investment(
    project: CharityProject,
    donation: Donation,
    amount: int
) -> None:
    project.invested_amount += amount
    donation.invested_amount += amount
    if project.invested_amount == project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    if donation.invested_amount == donation.full_amount:
        donation.fully_invested = True
        donation.close_date = datetime.now()
