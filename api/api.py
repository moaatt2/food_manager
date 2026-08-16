
#####################
### Imports/Setup ###
#####################

# ORM Imports
from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import select, create_engine, String, ForeignKey, exc, func, CTE
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session

# FastAPI Imports
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Path, Query, status, HTTPException

# Create Database engine
engine = create_engine("postgresql://test:test@localhost:5433/food")

# Tag descriptions for fast API docs
openapi_tags = [
    {"name": "Meals",          "description": "Meal methods"},
    {"name": "Post Methods",   "description": "Create new records"},
    {"name": "Get Methods",    "description": "Read records by ID"},
    {"name": "Put Methods",    "description": "Update records by ID"},
    {"name": "Delete Methods", "description": "Delete records by ID"},
]

# Create FastAPI App
app = FastAPI(
    title="Food Manager Backend",
    version="0.0.0",
    openapi_tags=openapi_tags
    )

# List of domains that can access API results
origins = [
    "http://localhost:5175",
]

# Use middleware to set up CORS headers for specified domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

### Create Models ###

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


### Update Models ###

class Meal_Update(BaseModel):
    name:       str | None             = None
    source:     str | None             = None
    type:       List[Meal_Type] | None = None
    num_meals:  int | None             = Field(ge=1, default=None)
    keeps_days: int | None             = Field(ge=1, default=None)


class Meal_Recipe_Update(BaseModel):
    recipe: str | None = None


class Meal_Review_Update(BaseModel):
    rating: int | None = Field(ge=1, le=5, default=None)
    review: str | None = None


class Meal_Note_Update(BaseModel):
    name: str | None = None
    note: str | None = None


class Ingredient_Update(BaseModel):
    name:         str | None = None
    keeps_days:   int | None = Field(ge=1, default=None)
    purchase_qty: str | None = None
    note:         str | None = None
    storage:      str | None = None


class Meal_Ingredient_Update(BaseModel):
    quantity: str | None = None


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


### Update ###

@app.put("/v1/meal/{meal_id}", tags=["Put Methods"])
async def update_meal(meal_id: Annotated[int, Path(title="Meal ID", gt=0, description="The ID of the meal you wish to update")], meal_data: Meal_Update):
    with Session(engine) as session:

        session.begin()

        # Fetch data from ORM
        stmt = select(Meal).where(Meal.id == meal_id)
        meal = session.scalars(stmt).one_or_none()

        # Handle missing meal
        if meal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal with that meal_id")

        # Update ORM object
        if meal_data.name is not None:
            meal.name = meal_data.name

        if meal_data.source is not None:
            meal.source = meal_data.source

        if meal_data.type is not None:
            meal.type = meal_data.type

        if meal_data.num_meals is not None:
            meal.num_meals = meal_data.num_meals

        if meal_data.keeps_days is not None:
            meal.keeps_days = meal_data.keeps_days

        # Mark record updated
        meal.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(meal)
        return {"meal": meal}


@app.put("/v1/recipe/{recipe_id}", tags=["Put Methods"])
async def update_recipe(recipe_id: Annotated[int, Path(title="Recipe ID", description="The ID of the recipe you wish to update")], recipe_data: Meal_Recipe_Update):
    with Session(engine) as session:
        session.begin()

        # Fetch Data from ORM
        stmt = select(Meal_Recipe).where(Meal_Recipe.id == recipe_id)
        recipe = session.scalars(stmt).one_or_none()

        # Handle missing recipe
        if recipe is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no recipe with that recipe_id")

        # Update ORM object
        if recipe_data.recipe is not None:
            recipe.recipe = recipe_data.recipe

        # Mark record updated
        recipe.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(recipe)
        return {"recipe": recipe}


@app.put("/v1/review/{review_id}", tags=["Put Methods"])
async def update_review(review_id: Annotated[int, Path(title="Review ID", description="The ID of the recipe you wish to update")], review_data: Meal_Review_Update):
    with Session(engine) as session:
        session.begin()

        # Fetch Data From ORM
        stmt = select(Meal_Review).where(Meal_Review.id == review_id)
        review = session.scalars(stmt).one_or_none()

        # Handle Missing Review
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no review with that review_id")

        # Update ORM object
        if review_data.rating is not None:
            review.rating = review_data.rating

        if review_data.review is not None:
            review.review = review_data.review

        # Mark record updated
        review.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(review)
        return {"review": review}


@app.put("/v1/note/{note_id}", tags=["Put Methods"])
async def update_note(note_id: Annotated[int, Path(title="Note ID", description="The ID of the note you wish to update")], note_data: Meal_Note_Update):
    with Session(engine) as session:
        session.begin()

        # Fetch data from ORM
        stmt = select(Meal_Note).where(Meal_Note.id == note_id)
        note = session.scalars(stmt).one_or_none()

        # Handle missing note
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no review with that review_id")

        # Update ORM object
        if note_data.name is not None:
            note.name = note_data.name

        if note_data.note is not None:
            note.note = note_data.note

        # Mark record updated
        note.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(note)
        return {"note": note}


@app.put("/v1/ingredient/{ingredient_id}", tags=["Put Methods"])
async def update_ingredient(ingredient_id: Annotated[int, Path(title="Ingredient ID", description="The ID of the ingredient you wish to update")], ingredient_data: Ingredient_Update):
    with Session(engine) as session:
        session.begin()

        # Fetch data from ORM
        stmt = select(Ingredient).where(Ingredient.id == ingredient_id)
        ingredient = session.scalars(stmt).one_or_none()

        # Handle missing ingredient
        if ingredient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no ingredient with that ingredient_id")

        # Update ORM object
        if ingredient_data.name is not None:
            ingredient.name = ingredient_data.name

        if ingredient_data.keeps_days is not None:
            ingredient.keeps_days = ingredient_data.keeps_days

        if ingredient_data.purchase_qty is not None:
            ingredient.purchase_qty = ingredient_data.purchase_qty

        if ingredient_data.note is not None:
            ingredient.note = ingredient_data.note

        if ingredient_data.storage is not None:
            ingredient.storage = ingredient_data.storage

        # Mark record updated
        ingredient.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(ingredient)
        return {"ingredient": ingredient}


@app.put("/v1/meal_ingredient/{meal_ingredient_id}", tags=["Put Methods"])
async def update_meal_ingredient(meal_ingredient_id: Annotated[int, Path(title="Meal Ingredient ID", description="The ID of the meal ingredient record you wish to update")], meal_ingredient_data: Meal_Ingredient_Update):
    with Session(engine) as session:
        session.begin()

        # Fetch ORM data
        stmt = select(Meal_Ingredient).where(Meal_Ingredient.id == meal_ingredient_id)
        meal_ingredient = session.scalars(stmt).one_or_none()

        # Handle Missing Ingredient
        if meal_ingredient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal_ingredient with that meal_ingredient_id")

        # Update ORM object
        if meal_ingredient_data.quantity is not None:
            meal_ingredient.quantity = meal_ingredient_data.quantity

        # Mark record updated
        meal_ingredient.updated_at = datetime.now()

        # Commit changes
        session.commit()

        # Update/return object
        session.refresh(meal_ingredient)
        return {"meal_ingredient": meal_ingredient}


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
            return {"message": f"Successfully deleted meal {meal_id}"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal with that meal_id")


@app.delete("/v1/recipe/{recipe_id}", tags=["Delete Methods"])
async def delete_recipe(recipe_id: Annotated[int, Path(title="Recipe ID", description="The ID of the recipe you wish to delete.")]):
    with Session(engine) as session:
        session.begin()

        # Get recipe
        stmt = select(Meal_Recipe).where(Meal_Recipe.id == recipe_id)
        recipe = session.scalars(stmt).one_or_none()

        # Handle missing recipe
        if recipe is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no recipe with that recipe_id")

        # Delete recipe
        session.delete(recipe)
        session.commit()
        return {"message": f"Successfully deleted recipe {recipe_id}"}


@app.delete("/v1/review/{review_id}", tags=["Delete Methods"])
async def delete_review(review_id: Annotated[int, Path(title="Review ID", description="The ID of the review you wish to delete.")]):
    with Session(engine) as session:
        session.begin()

        # Get review
        stmt = select(Meal_Review).where(Meal_Review.id == review_id)
        review = session.scalars(stmt).one_or_none()

        # Handle Missing Review
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no review with that review_id")

        # Delete Review
        session.delete(review)
        session.commit()
        return {"message": f"Successfully deleted review {review_id}"}


@app.delete("/v1/note/{note_id}", tags=["Delete Methods"])
async def delete_note(note_id: Annotated[int, Path(title="Note ID", description="The ID of the note you wish to delete.")]):
    with Session(engine) as session:
        session.begin()

        # Get Note
        stmt = select(Meal_Note).where(Meal_Note.id == note_id)
        note = session.scalars(stmt).one_or_none()

        # Handle missing note
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no note with that note_id")

        # Delete Note
        session.delete(note)
        session.commit()
        return {"message": f"Successfully deleted note {note_id}"}


@app.delete("/v1/ingredient/{ingredient_id}", tags=["Delete Methods"])
async def delete_ingredient(ingredient_id: Annotated[int, Path(title="Ingredient ID", description="The ID of the ingredient you wish to delete.")]):
    with Session(engine) as session:
        session.begin()

        # Get ingredient
        stmt = select(Ingredient).where(Ingredient.id == ingredient_id)
        ingredient = session.scalars(stmt).one_or_none()

        # Handle Missing Ingredient
        if ingredient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no ingredient with that ingredient_id")

        # Delete Ingredient
        session.delete(ingredient)
        session.commit()
        return {"message": f"Successfully deleted ingredient {ingredient_id}"}


@app.delete("/v1/meal_ingredient/{meal_ingredient_id}", tags=["Delete Methods"])
async def delete_meal_ingredient(meal_ingredient_id: Annotated[int, Path(title="Meal Ingredient ID", description="The ID of the meal ingredient you wish to delete.")]):
    with Session(engine) as session:
        session.begin()

        # Get Meal Ingredient
        stmt = select(Meal_Ingredient).where(Meal_Ingredient.id == meal_ingredient_id)
        meal_ingredient = session.scalars(stmt).one_or_none()

        # Handle Missing Meal Ingredient
        if meal_ingredient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no meal_ingredient with that meal_ingredient_id")

        # Delete Meal Ingredient
        session.delete(meal_ingredient)
        session.commit()
        return {"message": f"Successfully deleted meal ingredient {meal_ingredient_id}"}


### Search ###

@app.get("/v1/search/meals", tags=["Meals", "Get Methods"])
async def search_meals(
    ingredients_exclude: Annotated[List[int]       | None, Query(title="Ingredients Exclude", description="A list of igredient_ids for the ingredients you don't want in the meals")] = None,
    ingredients_include: Annotated[List[int]       | None, Query(title="Ingredients Include", description="A list of igredient_ids for the ingredients you want in the meals")] = None,
    types:               Annotated[List[Meal_Type] | None, Query(title="Types", description="The types of food you want to see")] = None,
    min_avg_review:      Annotated[float           | None, Query(title="Minimum Average Review", description="The minimum average review value of meals you want to see")] = None,
    limit:               Annotated[int             | None, Query(title="Limit",  description="The maximum number of results to return at once", ge=1, le=25)] = 10,
    cursor:              Annotated[int             | None, Query(title="Cursor", description="Enter a value here to get the next page of results if it exists", ge=0)] = None,
):
    with Session(engine) as session:
        session.begin()

        # Intial Query
        stmt = select(Meal).limit(limit).order_by(Meal.id.asc())

        # Handle Minimum Average Review
        if min_avg_review is not None:

            # Find the average reviews of all meals
            review_cte = select(Meal.id.label("meal_id"), func.avg(Meal_Review.rating).label("avg_review")).join(Meal_Review).group_by(Meal.id).limit(limit).cte(name="avg_reviews")

            # Apply the CTE to the query
            stmt = stmt.join(review_cte, review_cte.c.meal_id == Meal.id).where(review_cte.c.avg_review >= min_avg_review)

        # Handle Types
        if types is not None:
            stmt = stmt.where(Meal.type.overlap(types))

        # Handle including ingredients
        if ingredients_include is not None:

            # Find meals that have the desired ingredient
            ingredient_include_cte = select(Meal.id).distinct().join(Meal_Ingredient).where(Meal_Ingredient.ingredient_id.in_(ingredients_include)).cte(name="ingredient_include")

            # Filter to just meals with the desired ingredient
            stmt = stmt.join(ingredient_include_cte, ingredient_include_cte.c.id == Meal.id).where(Meal.id == ingredient_include_cte.c.id)

        # Handle exluding ingredients
        if ingredients_exclude is not None:

            # Find meals that have the unddesired ingredient
            ingredient_exclude_cte = select(Meal.id).distinct().join(Meal_Ingredient).where(Meal_Ingredient.ingredient_id.in_(ingredients_exclude)).cte(name="ingredient_exclude")

            # Filter to just meals without the undesired ingredient
            stmt = stmt.join(ingredient_exclude_cte, ingredient_exclude_cte.c.id == Meal.id, isouter=True).where(ingredient_exclude_cte.c.id == None)


        # Handle Cursor
        if cursor:
            stmt = stmt.filter(Meal.id > cursor)

        # Get Results
        meals = session.scalars(stmt).all()

        return {
            "meals": meals,
            "next_cursor": meals[-1].id if meals else None
        }


