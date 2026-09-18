import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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

    snapshots = relationship("OddsSnapshot", back_populates="match")

class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    bookmaker = Column(String)
    outcome = Column(String)
    price = Column(Float)
    recorded_at = Column(DateTime)

    match = relationship("Match", back_populates="snapshots")

Base.metadata.create_all(engine)