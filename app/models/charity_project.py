from sqlalchemy import Column, String, Text

from app.models.base import BaseModel
from app.models.constants import (CHARITY_PROJECT_NAME_MAX_LENGTH,
                                  CHARITY_PROJECT_NAME_MIN_LENGTH)


class CharityProject(BaseModel):
    name = Column(String(CHARITY_PROJECT_NAME_MAX_LENGTH),
                  unique=True, nullable=False)
    description = Column(Text(CHARITY_PROJECT_NAME_MIN_LENGTH),
                         nullable=False)
