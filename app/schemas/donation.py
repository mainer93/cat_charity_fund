from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.models.constants import DEFAULT_INVESTED_AMOUNT


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreateResponse(BaseModel):
    id: int
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class DonationMyDB(DonationCreate):
    id: int
    create_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class DonationDB(DonationMyDB):
    user_id: Optional[int]
    invested_amount: int = DEFAULT_INVESTED_AMOUNT
    fully_invested: bool = False
    close_date: datetime = None
