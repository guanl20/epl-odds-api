import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    api_match_id = Column(String, unique=True)
    home_team = Column(String)
    away_team = Column(String)
    commence_time = Column(DateTime)

class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    bookmaker = Column(String)
    outcome = Column(String)
    price = Column(Float)
    recorded_at = Column(DateTime)

Base.metadata.create_all(engine)