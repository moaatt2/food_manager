
-- Create Schema
CREATE SCHEMA test_schema;

-- Create table
CREATE TABLE test_catalog.test_schema.test_table_2 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
);
