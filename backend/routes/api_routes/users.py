from fastapi import APIRouter, Form
from pydantic import BaseModel
from dataclasses import dataclass

router = APIRouter(prefix="/users", tags=["users"])

@dataclass
class User:
    userName: str
    firstName: str
    lastName: str
    email: str
    password: str

@router.post("/create_user")
async def create_user(
    userName: str = Form(...),
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = User(userName, firstName, lastName, email, password)
    return {"created_user": user.__dict__}