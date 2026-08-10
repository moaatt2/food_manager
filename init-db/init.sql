
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
    purchase_qty VARCHAR(10),
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
    rating INTEGER,
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

