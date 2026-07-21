from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key = True)
    strava_id = Column(String, unique=True) # never accidentally import exact same workout twice from Strava
    activity_type = Column(String)          # "Run", "Ride", "Swim", "WeightTraining", etc.
    name = Column(String)                   # e.g. "Morning Run"
    distance_meters = Column(Float)
    duration_seconds = Column(Integer)
    elevation_gain_meters = Column(Float)
    average_heartrate = Column(Float, nullable=True)
    start_date = Column(DateTime)

    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)  
    goal = relationship("Goal", back_populates="activities")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    race_type = Column(String)      # "5k", "10k", "half_marathon", "marathon", "ironman_70_3", "hyrox", etc.
    race_name = Column(String, nullable=True)
    race_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    activities = relationship("Activity", back_populates="goal")
    notes = relationship("CoachingNote", back_populates="goal")

class CoachingNote(Base):
    __tablename__ = "coaching_notes"

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    week_start = Column(DateTime)
    content = Column(String)         # the LLM-generated coaching text
    risk_flag = Column(String)       # "none", "overtraining", "undertraining", "on_track"
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("Goal", back_populates="notes")
