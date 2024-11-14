from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.models.constants import (CHARITY_PROJECT_DESCRIPTION_MIN_LENGTH,
                                  CHARITY_PROJECT_NAME_MAX_LENGTH,
                                  CHARITY_PROJECT_NAME_MIN_LENGTH,
                                  DEFAULT_INVESTED_AMOUNT)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None,
                                min_length=CHARITY_PROJECT_NAME_MIN_LENGTH,
                                max_length=CHARITY_PROJECT_NAME_MAX_LENGTH)
    description: Optional[str] = Field(
        None,
        min_length=CHARITY_PROJECT_DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=CHARITY_PROJECT_NAME_MIN_LENGTH,
                      max_length=CHARITY_PROJECT_NAME_MAX_LENGTH)
    description: str = Field(min_length=CHARITY_PROJECT_DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = DEFAULT_INVESTED_AMOUNT
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
