import sqlalchemy

# Connect to database and create connection
engine = sqlalchemy.create_engine("postgresql://test:test@localhost:5433/food")
with engine.connect() as connection:

    # Begin connection for safety
    connection.begin()

    # Run query on database and print results
    cursor = connection.exec_driver_sql("SELECT * FROM INFORMATION_SCHEMA.TABLES LIMIT 10;")
    for row in cursor._allrows():
        print(row)

    # Ensure no changes remain
    connection.rollback()
