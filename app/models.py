from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# Association model for jobs a user has applied to
class JobApplication(Base):
    __tablename__ = 'jobs_applied_to'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="jobs_applied_to")
    job = relationship("Job", back_populates="applied_users")


# Association model for jobs a user is interested in (liked)
class JobInterest(Base):
    __tablename__ = 'jobs_interested_in'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="jobs_interested_in")
    job = relationship("Job", back_populates="interested_users")


# User model representing the users on the platform
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    university = Column(String, nullable=False)
    course = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    skills = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Relationships
    jobs = relationship("Job", back_populates="user")  # Jobs posted by the user
    bookmarks = relationship("Bookmark", back_populates="user")  # Jobs bookmarked by the user
    jobs_applied_to = relationship("JobApplication", back_populates="user")  # Jobs the user has applied to
    jobs_interested_in = relationship("JobInterest", back_populates="user")  # Jobs the user is interested in


# Job posting model
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    posted_at = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="jobs")
    bookmarks = relationship("Bookmark", back_populates="job")
    applied_users = relationship("JobApplication", back_populates="job")  # Users who applied for this job
    interested_users = relationship("JobInterest", back_populates="job")  # Users interested in this job


# Bookmark model
class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    job = relationship("Job", back_populates="bookmarks")
