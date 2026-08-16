from bson import ObjectId
from app.database import get_database
from app.models import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.errors import (
    DuplicateEmailException,
    InvalidCredentialsException,
    UserNotFoundException,
)


class AuthService:
    def __init__(self):
        self.db = get_database()
        self.users_collection = self.db["users"]

    def register(self, name: str, email: str, password: str) -> User:
        # Check if email already exists
        existing_user = self.users_collection.find_one({"email": email})
        if existing_user:
            raise DuplicateEmailException()

        # Hash password and create user
        password_hash = hash_password(password)
        user = User(name=name, email=email, password_hash=password_hash)

        # Insert into database
        result = self.users_collection.insert_one(user.to_dict())
        user._id = result.inserted_id
        return user

    def login(self, email: str, password: str) -> tuple[User, str]:
        # Find user by email
        user_doc = self.users_collection.find_one({"email": email})
        if not user_doc:
            raise InvalidCredentialsException()

        # Verify password
        if not verify_password(password, user_doc["password_hash"]):
            raise InvalidCredentialsException()

        user = User.from_dict(user_doc)

        # Create token
        token = create_access_token({"sub": str(user._id), "email": email})

        return user, token

    def get_user_by_id(self, user_id: str) -> User:
        try:
            obj_id = ObjectId(user_id)
        except Exception:
            raise UserNotFoundException()

        user_doc = self.users_collection.find_one({"_id": obj_id})
        if not user_doc:
            raise UserNotFoundException()

        return User.from_dict(user_doc)

    def get_user_by_email(self, email: str) -> User:
        user_doc = self.users_collection.find_one({"email": email})
        if not user_doc:
            raise UserNotFoundException()

        return User.from_dict(user_doc)
