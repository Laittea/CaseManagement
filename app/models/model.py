from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class UserRole(PyEnum):
    RECRUITER = "recruiter"
    ADMIN = "admin"
    CANDIDATE = "candidate"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    candidate = relationship("Candidate", back_populates="user", cascade="all, delete", passive_deletes=True)
    recruiter = relationship("Recruiter", back_populates="user", cascade="all, delete", passive_deletes=True)
    admin = relationship("Admin", back_populates="user", cascade="all, delete", passive_deletes=True)


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    application_date = Column(DateTime, nullable=False)
    application_status = Column(String, nullable=False)
    user = relationship("User", back_populates="candidate")
    detailed_info = relationship("DetailedInfo", back_populates="candidate", cascade="all, delete-orphan", passive_deletes=True)


class Recruiter(Base):
    __tablename__ = "recruiters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="recruiter")


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="admin")


class DetailedInfo(Base):
    __tablename__ = "detailed_info"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    candidate = relationship("Candidate", back_populates="detailed_info")
    attending_school = Column(String)
    level_of_schooling = Column(String)
    fluent_english_scale = Column(String)
    reading_english_scale = Column(Integer)
    speaking_english_scale = Column(Integer)
    writing_english_scale = Column(Integer)
    numeracy_scale = Column(Integer)
    computer_scale = Column(Integer)
    work_experience = Column(Integer)
    canada_work_ex = Column(Integer)
    currently_employed = Column(String)
    income_source = Column(String)
    time_unemployed = Column(Integer)
    substance_use = Column(String)
    caregiver_bool = Column(String)
    housing_bool = Column(String)
    need_mental_health_support_bool = Column(String)
    transportation_bool = Column(String)
    felony_bool = Column(String)
