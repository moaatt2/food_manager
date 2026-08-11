
from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import select, create_engine, String, ForeignKey
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
    type:       Mapped[List[str]] = mapped_column(ARRAY(String))
    num_meals:  Mapped[int]
    keeps_days: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Meal(id={self.id!r}, name={self.name!r}, type={self.type!r})"


class Meal_Recipe(Base):
    __tablename__ = "meal_recipies"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]    = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"] = mapped_column(ForeignKey("food.meals.id"))
    recipe:     Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Recipe(id={self.id!r}, meal_id={self.meal_id!r}, created_at={self.created_at!r}, updated_at={self.created_at!r})"


# Create Engine/Session
engine = create_engine("postgresql://test:test@localhost:5433/food")
with Session(engine) as session:

    # Single Table Query
    stmt = select(Meal).where(Meal.id == 1)
    for meal in session.scalars(stmt):
        print(meal)

    # Multi Table Query
    stmt = select(Meal_Recipe).join(Meal).where(Meal.type.any('Lunch'))
    for recipe in session.scalars(stmt):
        print(recipe)
