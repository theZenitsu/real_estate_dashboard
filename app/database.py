from sqlalchemy import create_engine
import pandas as pd

# Replace with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:anass@localhost:5432/real_estate"

# Create the database engine
engine = create_engine(DATABASE_URL)

def fetch_data(query, params=None):
    """
    Execute a SQL query and return the results as a pandas DataFrame.
    """
    with engine.connect() as connection:
        return pd.read_sql_query(query, connection, params=params)
