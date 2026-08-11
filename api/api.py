
from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session

# Base Class
class Base(DeclarativeBase):
    pass


class Meal(Base):
    __tablename__ = "meals"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int] = mapped_column(primary_key=True)
    name:       Mapped[str]
    source:     Mapped[str]
    num_meals:  Mapped[int]
    keeps_days: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Meal(id={self.id!r}, name={self.name!r})"

# Create Engine/Session
engine = create_engine("postgresql://test:test@localhost:5433/food")
with Session(engine) as session:

    stmt = select(Meal).where(Meal.id == 1)

    for meal in session.scalars(stmt):
        print(meal)



