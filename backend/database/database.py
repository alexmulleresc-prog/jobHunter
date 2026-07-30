from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

DATABASE_URL = (f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)