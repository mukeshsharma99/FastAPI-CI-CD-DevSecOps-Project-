from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

import os


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://fastapi:fastapi_password@localhost:5432/fastapi_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# --------------------------------------------------
# Database Model
# --------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)


# Create tables
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(title="FastAPI CI/CD Project")


# --------------------------------------------------
# Pydantic Schema
# --------------------------------------------------

class UserCreate(BaseModel):
    name: str
    email: str


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "FastAPI + PostgreSQL is working"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Get All Users
# --------------------------------------------------

@app.get("/users")
def get_users():
    db = SessionLocal()

    try:
        users = db.query(User).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in users
        ]

    finally:
        db.close()


# --------------------------------------------------
# Create User
# --------------------------------------------------

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        new_user = User(
            name=user.name,
            email=user.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }

    finally:
        db.close()


# --------------------------------------------------
# Get User By ID
# --------------------------------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    finally:
        db.close()


# --------------------------------------------------
# Update User
# --------------------------------------------------

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserCreate):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Check duplicate email
        existing_user = (
            db.query(User)
            .filter(
                User.email == user_data.email,
                User.id != user_id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        user.name = user_data.name
        user.email = user_data.email

        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    finally:
        db.close()


# --------------------------------------------------
# Delete User
# --------------------------------------------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }

    finally:
        db.close()