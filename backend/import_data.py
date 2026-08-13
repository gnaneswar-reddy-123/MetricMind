from pathlib import Path
import pandas as pd
from sqlalchemy import text
from app.database import engine

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR.parent / "dataset" / "sales_data.csv"

df = pd.read_csv(CSV_FILE)

print(f"CSV rows found: {len(df)}")

with engine.begin() as connection:
    connection.execute(text("DELETE FROM sales"))

df.to_sql(
    name="sales",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print(f"Successfully imported {len(df)} rows into metricmind_db.sales")