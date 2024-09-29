from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Shared base model for User
class UserBase(BaseModel):
    email: EmailStr
    university: str
    course: str
    semester: str
    skills: str


# Model for creating a new user (e.g., during registration)
class UserCreate(UserBase):
    password: str


# Response model for reading user data
class UserResponse(UserBase):
    id: int
    created_at: datetime
    jobs_applied_to: Optional[List["JobResponse"]] = []  # Changed to JobResponse to match the job data
    jobs_interested_in: Optional[List["JobResponse"]] = []  # Changed to JobResponse to match the job data

    class Config:
        orm_mode = True


# Shared base model for Job
class JobBase(BaseModel):
    title: str
    description: str
    company_name: str


# Model for creating a new job
class JobCreate(JobBase):
    pass


# Response model for reading job data
class JobResponse(JobBase):
    id: int
    user_id: int
    posted_at: datetime
    bookmarks: Optional[List["BookmarkResponse"]] = []  # Changed to BookmarkResponse for consistency

    class Config:
        orm_mode = True


# Shared base model for Bookmark
class BookmarkBase(BaseModel):
    pass


# Model for creating a new bookmark
class BookmarkCreate(BookmarkBase):
    job_id: int
    user_id: int


# Response model for reading bookmark data
class BookmarkResponse(BookmarkBase):
    id: int
    job_id: int
    user_id: int

    class Config:
        orm_mode = True


# Define Job Application Response
class JobsAppliedTo(BaseModel):
    job_id: int
    user_id: int

    class Config:
        orm_mode = True


# Define Job Interest Response (Liked Jobs)
class JobsInterestedIn(BaseModel):
    job_id: int
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode = True
