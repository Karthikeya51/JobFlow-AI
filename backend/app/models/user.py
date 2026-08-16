from datetime import datetime
from bson import ObjectId


class User:
    def __init__(
        self,
        name: str,
        email: str,
        password_hash: str,
        created_at: datetime = None,
        _id: ObjectId = None,
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )
