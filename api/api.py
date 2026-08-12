
#####################
### Imports/Setup ###
#####################

# ORM Imports
from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import select, create_engine, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session

# FastAPI Imports
from typing import Annotated
from fastapi import FastAPI, Path, status, HTTPException

# Create Database engine
engine = create_engine("postgresql://test:test@localhost:5433/food")

# Tag descriptions for fast API docs
openapi_tags = [
    {"name": "Get Methods", "description": "Get Records by ID"}
]

# Create FastAPI App
app = FastAPI(
    title="Food Manager Backend",
    version="0.0.0",
    openapi_tags=openapi_tags
    )


######################
### Create Objects ###
######################

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
    __tablename__ = "meal_recipes"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]    = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"] = mapped_column(ForeignKey("food.meals.id"))
    recipe:     Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Recipe(id={self.id!r}, meal_id={self.meal_id!r}, created_at={self.created_at!r}, updated_at={self.created_at!r})"


class Meal_Review(Base):
    __tablename__ = "meal_reviews"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]    = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"] = mapped_column(ForeignKey("food.meals.id"))
    rating:     Mapped[int]
    review:     Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Review(id={self.id!r}, meal_id={self.meal_id!r}, rating={self.rating!r})"


class Meal_Note(Base):
    __tablename__  = "meal_notes"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]    = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"] = mapped_column(ForeignKey("food.meals.id"))
    name:       Mapped[str]
    note:       Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Note(id={self.id!r}, meal_id={self.meal_id!r}, name={self.name!r}, note={self.note!r})"


class Ingredient(Base):
    __tablename__  = "ingredients"
    __table_args__ = {"schema": "food"}

    id:           Mapped[int] = mapped_column(primary_key=True)
    name:         Mapped[str]
    keeps_days:   Mapped[int]
    purchase_qty: Mapped[str]
    note:         Mapped[str]
    storage:      Mapped[str]
    created_at:   Mapped[datetime]
    updated_at:   Mapped[datetime]
    deleted_at:   Mapped[Optional[datetime]]


class Meal_Ingredient(Base):
    __tablename__  = "meal_ingredients"
    __table_args__ = {"schema": "food"}

    id:            Mapped[int]          = mapped_column(primary_key=True)
    meal_id:       Mapped["Meal"]       = mapped_column(ForeignKey("food.meals.id"))
    ingredient_id: Mapped["Ingredient"] = mapped_column(ForeignKey("food.ingredients.id"))
    quantity:      Mapped[str]
    created_at:    Mapped[datetime]
    updated_at:    Mapped[datetime]
    deleted_at:    Mapped[Optional[datetime]]


#####################
### API Endpoints ###
#####################

### Getters ###

@app.get("/v1/meal/{meal_id}", tags=["Get Methods"])
async def get_meal(meal_id: Annotated[int, Path(title="Meal ID", gt=0, description="The ID of the meal you wish to fetch.")]):
    with Session(engine) as session:

        # Query to find meal
        stmt = select(Meal).where(Meal.id == meal_id)

        # Query Result
        meal = session.scalars(stmt).one_or_none()

        if meal is not None:
            return {"meal": meal}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal with that meal_id")


@app.get("/v1/recipe/{recipe_id}", tags=["Get Methods"])
async def get_recipe(recipe_id: Annotated[int, Path(title="Recipe ID", gt=0, description="The ID of the recipe you wish to fetch.")]):
    with Session(engine) as session:

        # Query to find meal
        stmt = select(Meal_Recipe).where(Meal_Recipe.id == recipe_id)

        # Query Result
        recipe = session.scalars(stmt).one_or_none()

        if recipe is not None:
            return {"recipe": recipe}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no recipe with that recipe_id")


@app.get("/v1/review/{review_id}", tags=["Get Methods"])
async def get_review(review_id: Annotated[int, Path(title="Review ID", gt=0, description="The ID of the review you wish to fetch.")]):
    with Session(engine) as session:

        # Query to find meal
        stmt = select(Meal_Review).where(Meal_Review.id == review_id)

        # Query Result
        review = session.scalars(stmt).one_or_none()

        if review is not None:
            return {"review": review}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no review with that review_id")


@app.get("/v1/note/{note_id}", tags=["Get Methods"])
async def get_note(note_id: Annotated[int, Path(title="Note ID", gt=0, description="The ID of the note you wish to fetch.")]):
    with Session(engine) as session:

        # Query to find meal
        stmt = select(Meal_Note).where(Meal_Note.id == note_id)

        # Query Result
        note = session.scalars(stmt).one_or_none()

        if note is not None:
            return {"note": note}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no note with that note_id")


@app.get("/v1/ingredient/{ingredient_id}", tags=["Get Methods"])
async def get_note(ingredient_id: Annotated[int, Path(title="Ingredient ID", gt=0, description="The ID of the ingredient you wish to fetch.")]):
    with Session(engine) as session:

        # Query to find meal
        stmt = select(Ingredient).where(Ingredient.id == ingredient_id)

        # Query Result
        ingredient = session.scalars(stmt).one_or_none()

        if ingredient is not None:
            return {"ingredient": ingredient}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no ingredient with that ingredient_id")



