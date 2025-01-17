from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.enums import Role


class UserSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str
    phone_number: str
    role: Role

    @field_validator("phone_number")
    def validate_phone(cls, p):
        try:
            if p.isdigit() and len(p) == 10:
                return f"38{p}"
        except ValueError:
            raise ValueError("Invalid phone  format. Phone must be 10 digits.")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserDetail(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: Role

    class Config:
        from_attributes = True
