from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv("APP_ENV", "dev")
load_dotenv(f".env.{env}")

creedentials = {
    "driver": os.getenv("DB_DRIVER"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_DATABASE"),
}

SQLALCHEMY_DATABASE_URL = f"{creedentials['driver']}+pymysql://{creedentials['user']}:{creedentials['password']}@{creedentials['host']}:{creedentials['port']}/{creedentials['database']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
