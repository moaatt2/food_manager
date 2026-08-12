
#####################
### Imports/Setup ###
#####################

# ORM Imports
from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import select, create_engine, String, ForeignKey, exc
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session

# FastAPI Imports
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Path, status, HTTPException

# Create Database engine
engine = create_engine("postgresql://test:test@localhost:5433/food")

# Tag descriptions for fast API docs
openapi_tags = [
    {"name": "Get Methods",    "description": "Get records by ID"},
    {"name": "Post Methods",   "description": "Create new records"},
    {"name": "Delete Methods", "description": "Delete records by ID"}
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

    id:         Mapped[int]       = mapped_column(primary_key=True)
    name:       Mapped[str]
    source:     Mapped[str]
    type:       Mapped[List[str]] = mapped_column(ARRAY(String))
    num_meals:  Mapped[int]
    keeps_days: Mapped[int]
    created_at: Mapped[datetime]  = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime]  = mapped_column(default=datetime.now())
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Meal(id={self.id!r}, name={self.name!r}, type={self.type!r})"


class Meal_Recipe(Base):
    __tablename__ = "meal_recipes"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]      = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"]   = mapped_column(ForeignKey("food.meals.id"))
    recipe:     Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Recipe(id={self.id!r}, meal_id={self.meal_id!r}, created_at={self.created_at!r}, updated_at={self.created_at!r})"


class Meal_Review(Base):
    __tablename__ = "meal_reviews"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]      = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"]   = mapped_column(ForeignKey("food.meals.id"))
    rating:     Mapped[int]
    review:     Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Review(id={self.id!r}, meal_id={self.meal_id!r}, rating={self.rating!r})"


class Meal_Note(Base):
    __tablename__  = "meal_notes"
    __table_args__ = {"schema": "food"}

    id:         Mapped[int]      = mapped_column(primary_key=True)
    meal_id:    Mapped["Meal"]   = mapped_column(ForeignKey("food.meals.id"))
    name:       Mapped[str]
    note:       Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self):
        return f"Note(id={self.id!r}, meal_id={self.meal_id!r}, name={self.name!r}, note={self.note!r})"


class Ingredient(Base):
    __tablename__  = "ingredients"
    __table_args__ = {"schema": "food"}

    id:           Mapped[int]      = mapped_column(primary_key=True)
    name:         Mapped[str]
    keeps_days:   Mapped[int]
    purchase_qty: Mapped[str]
    note:         Mapped[str]
    storage:      Mapped[str]
    created_at:   Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at:   Mapped[datetime] = mapped_column(default=datetime.now())
    deleted_at:   Mapped[Optional[datetime]]


class Meal_Ingredient(Base):
    __tablename__  = "meal_ingredients"
    __table_args__ = {"schema": "food"}

    id:            Mapped[int]          = mapped_column(primary_key=True)
    meal_id:       Mapped["Meal"]       = mapped_column(ForeignKey("food.meals.id"))
    ingredient_id: Mapped["Ingredient"] = mapped_column(ForeignKey("food.ingredients.id"))
    quantity:      Mapped[str]
    created_at:    Mapped[datetime]     = mapped_column(default=datetime.now())
    updated_at:    Mapped[datetime]     = mapped_column(default=datetime.now())
    deleted_at:    Mapped[Optional[datetime]]


########################
### API Models/Enums ###
########################

# Enum to limit meal types
class Meal_Type(str, Enum):
    breakfast = "Breakfast"
    lunch     = "Lunch"
    dinner    = "Dinner"
    desert    = "Desert"


class Meal_Create(BaseModel):
    name:       str
    source:     str | None      = None
    type:       List[Meal_Type]
    num_meals:  int             = Field(ge=1, default=1)
    keeps_days: int             = Field(ge=1, default=1)


class Meal_Recipe_Create(BaseModel):
    meal_id: int
    recipe:  str


class Meal_Review_Create(BaseModel):
    meal_id: int
    rating:  int = Field(ge=1, le=5)
    review:  str | None = None


class Meal_Note_Create(BaseModel):
    meal_id: int
    name:    str
    note:    str


class Ingredient_Create(BaseModel):
    name:         str
    keeps_days:   int = Field(ge=1)
    purchase_qty: str
    note:         str | None = None
    storage:      str


class Meal_Ingredient_Create(BaseModel):
    meal_id:       int
    ingredient_id: int
    quantity:      str


#####################
### API Endpoints ###
#####################

### Create ###

@app.post("/v1/meal", tags=["Post Methods"])
async def create_meal(meal_data: Meal_Create):
    with Session(engine) as session:

        # Create ORM object
        meal = Meal(
            id         = None,
            name       = meal_data.name,
            source     = meal_data.source,
            type       = meal_data.type,
            num_meals  = meal_data.num_meals,
            keeps_days = meal_data.keeps_days,
        )

        # Push object to database
        session.begin()
        session.add(meal)
        session.commit()

        # Update object and return to user
        session.refresh(meal)
        return {"meal": meal}


@app.post("/v1/recipe", tags=["Post Methods"])
async def create_recipe(recipe_data:Meal_Recipe_Create):
    with Session(engine) as session:
        try:

            # Create ORM object
            recipe = Meal_Recipe(
                id      = None,
                meal_id = recipe_data.meal_id,
                recipe  = recipe_data.recipe
            )

            # Push row to database
            session.begin()
            session.add(recipe)
            session.commit()

            # Update object and return to user
            session.refresh(recipe)
            return {"recipe": recipe}

        except exc.IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"SQLAlchemy Itegrity Error {e._message()}")


@app.post("/v1/review", tags=["Post Methods"])
async def create_review(review_data: Meal_Review_Create):
    with Session(engine) as session:
        try:

            # Create ORM Object
            review = Meal_Review(
                id      = None,
                meal_id = review_data.meal_id,
                rating  = review_data.rating,
                review  = review_data.review,
            )

            # Push row to database
            session.begin()
            session.add(review)
            session.commit()

            # Update ojbect and return to use
            session.refresh(review)
            return {"review": review}

        except exc.IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"SQLAlchemy Itegrity Error {e._message()}")

@app.post("/v1/note", tags=["Post Methods"])
async def create_note(note_data: Meal_Note_Create):
    with Session(engine) as session:
        try:

            # Create ORM object
            note = Meal_Note(
                id      = None,
                meal_id = note_data.meal_id,
                name    = note_data.name,
                note    = note_data.note
            )

            # Push row to database
            session.begin()
            session.add(note)
            session.commit()

            # Update ojbect and return to use
            session.refresh(note)
            return {"note": note}

        except exc.IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"SQLAlchemy Itegrity Error {e._message()}")


@app.post("/v1/ingredient", tags=["Post Methods"])
async def create_ingredient(ingredient_data: Ingredient_Create):
    with Session(engine) as session:

        # Create ORM Object
        ingredient = Ingredient(
            id           = None,
            name         = ingredient_data.name,
            keeps_days   = ingredient_data.keeps_days,
            purchase_qty = ingredient_data.purchase_qty,
            note         = ingredient_data.note,
            storage      = ingredient_data.storage,
        )

        # Push object to database
        session.begin()
        session.add(ingredient)
        session.commit()

        # Update object and return to user
        session.refresh(ingredient)
        return {"ingredient": ingredient}


@app.post("/v1/meal_ingredient", tags=["Post Methods"])
async def create_meal_ingredient(meal_ingredient_data: Meal_Ingredient_Create):
    with Session(engine) as session:
        try:

            # Create ORM object
            meal_ingredient = Meal_Ingredient(
                id            = None,
                meal_id       = meal_ingredient_data.meal_id,
                ingredient_id = meal_ingredient_data.ingredient_id,
                quantity      = meal_ingredient_data.quantity,
            )

            # Push row to database
            session.begin()
            session.add(meal_ingredient)
            session.commit()

            # Update ojbect and return to use
            session.refresh(meal_ingredient)
            return {"meal_ingredient": meal_ingredient}

        except exc.IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"SQLAlchemy Itegrity Error {e._message()}")


@app.post("/v1/meal_ingredients", tags=["Post Methods"])
async def create_meal_ingredients(meal_ingredients_data: List[Meal_Ingredient_Create]):
    with Session(engine) as session:
        try:

            # Begin transaction
            session.begin()

            ingredients = list()
            for ingredient in meal_ingredients_data:

                # Create ORM Object
                meal_ingredient = Meal_Ingredient(
                    id            = None,
                    meal_id       = ingredient.meal_id,
                    ingredient_id = ingredient.ingredient_id,
                    quantity      = ingredient.quantity,
                )
                session.add(meal_ingredient)
                ingredients.append(meal_ingredient)

            # Commit Transaction
            session.commit()
            _ = [session.refresh(i) for i in ingredients]

            # Update objects and return
            return ingredients


        except exc.IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"SQLAlchemy Itegrity Error {e._message()}")


### Read ###

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


### Delete ###

@app.delete("/v1/meal/{meal_id}", tags=["Delete Methods"])
async def delete_meal(meal_id: Annotated[int, Path(title="Meal ID", gt=0, description="The ID of the meal you wish to delete.")]):
    with Session(engine) as session:

        # Initialize session
        session.begin()

        # Query to find meal
        stmt = select(Meal).where(Meal.id == meal_id)

        # Query Result
        meal = session.scalars(stmt).one_or_none()

        if meal is not None:
            session.delete(meal)
            session.commit()
            return {"message": f"Sucesfully deleted meal {meal_id}"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal with that meal_id")



