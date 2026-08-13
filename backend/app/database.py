from sqlalchemy import create_engine
from urllib.parse import quote_plus

PASSWORD = "gnaneswar@123"

DATABASE_URL = (
    f"mysql+pymysql://root:{quote_plus(PASSWORD)}@localhost:3306/metricmind_db"
)

engine = create_engine(DATABASE_URL)