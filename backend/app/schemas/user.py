from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepassword123",
            }
        }


class UserResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    created_at: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2024-01-15T10:30:00",
            }
        }


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserResponseSchema

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "created_at": "2024-01-15T10:30:00",
                },
            }
        }
