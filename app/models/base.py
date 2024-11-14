from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base
from app.models.constants import DEFAULT_INVESTED_AMOUNT


class BaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0',
                        name='check_full_amount_positive'),
        CheckConstraint('invested_amount <= full_amount',
                        name='check_invested_not_exceed_full_amount'),
    )
