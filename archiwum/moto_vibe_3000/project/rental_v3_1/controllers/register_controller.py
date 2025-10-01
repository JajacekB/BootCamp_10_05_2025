from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, EmailStr, validator
import bcrypt

from models.user import User
from repositories.write_methods import add_user
from repositories.read_methods import get_user_by
from database import SessionLocal

app = FastAPI()


class RegisterData(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    street: str
    post_code: str
    city: str
    country: str
    login: str
    password: str
    confirm_password: str

    @validator('password')
    def password_valid(cls, v):
        if len(v) < 6 or not any(c.isupper() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('Hasło musi mieć min 6 znaków, 1 wielką literę i 1 cyfrę.')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Hasła nie są zgodne.')
        return v


@app.post("/api/register")
async def register_user(data: RegisterData):
    session = SessionLocal()
    try:
        existing = get_user_by(session, login=data.login)
        if existing:
            return JSONResponse({"success": False, "message": "Użytkownik o takim loginie już istnieje."})

        password_hash = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode()

        new_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            login=data.login,
            phone=data.phone,
            email=data.email,
            password_hash=password_hash,
            address=f"{data.street}, {data.post_code} {data.city}, {data.country}",
            role="client"
        )

        success, text = add_user(session, new_user)
        return {"success": success, "message": text}

    finally:
        session.close()


@app.get("/register")
async def register_page():
    return FileResponse("static/register.html")
