from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dependencies.read_env import getenv

creedentials = {
    "driver": getenv("DB_DRIVER"),
    "user": getenv("DB_USERNAME"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
    "database": getenv("DB_DATABASE"),
}

SQLALCHEMY_DATABASE_URL = f"{creedentials['driver']}+pymysql://{creedentials['user']}:{creedentials['password']}@{creedentials['host']}:{creedentials['port']}/{creedentials['database']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
