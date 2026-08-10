
--------------------------
--- Create Food Tables ---
--------------------------

CREATE SCHEMA food;


CREATE TABLE food.food.meals (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50),
    source     VARCHAR(50) DEFAULT NULL,
    type       VARCHAR(10) [],
    num_meals  INTEGER,
    keeps_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);


CREATE TABLE food.food.ingredients (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(50),
    keeps_days   INTEGER,
    purchase_qty VARCHAR(25),
    note         TEXT DEFAULT NULL,
    storage      VARCHAR(10),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at   TIMESTAMP DEFAULT NULL
);


CREATE TABLE food.food.meal_recipies (
    id SERIAL  PRIMARY KEY,
    meal_id    INTEGER,
    recipe     TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_meal
        FOREIGN KEY(meal_id)
            REFERENCES food.food.meals(id)
);


CREATE TABLE food.food.meal_ingredients (
    id SERIAL PRIMARY KEY,
    meal_id INTEGER,
    ingredient_id INTEGER,
    quantity VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_meal
        FOREIGN KEY(meal_id)
            REFERENCES food.food.meals(id),
    CONSTRAINT fk_ingredient
        FOREIGN KEY(ingredient_id)
            REFERENCES food.food.ingredients(id)
);


CREATE TABLE food.food.meal_reviews (
    id SERIAL PRIMARY KEY,
    meal_id INTEGER,
    rating INTEGER CONSTRAINT review_in_range CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_meal
        FOREIGN KEY(meal_id)
            REFERENCES food.food.meals(id)
);


CREATE TABLE food.food.meal_notes (
    id SERIAL PRIMARY KEY,
    meal_id INTEGER,
    name VARCHAR(50),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_meal
        FOREIGN KEY(meal_id)
            REFERENCES food.food.meals(id)
);


-----------------
--- Seed Data ---
-----------------

INSERT INTO food.food.meals (id, name, type, num_meals, keeps_days)
    VALUES (
        1,
        'Boiled Chicken',
        '{"Lunch", "Dinner"}',
        1,
        3
    );

INSERT INTO food.food.ingredients (id, name, keeps_days, purchase_qty, storage)
    VALUES (
        1,
        'chicken breast',
        3,
        '1 Breast',
        'Freezer'
    );

INSERT INTO food.food.meal_recipies (meal_id, recipe)
    VALUES (
        1,
        '1. Put desired number of chicken breasts in an oven safe container.\n2. Fill container with water.\n3. Preheat oven to ???.\n4. Cook chicken in oven for ?? minutes.'
    );

INSERT INTO food.food.meal_ingredients (meal_id, ingredient_id, quantity)
    VALUES (
        1,
        1,
        '1 Breast'
    );

INSERT INTO food.food.meal_reviews (meal_id, rating, review)
    VALUES (
        1,
        2,
        'Quite boring, only gets a 2 because it is easy to make.'
    );

INSERT INTO food.food.meal_notes (meal_id, name, note)
    VALUES (
        1,
        'Dakota',
        'Add 1 tsp salt next time.'
    );
