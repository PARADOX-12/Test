from db import db
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from datetime import datetime

class UserModel(object):
    def __init__(self, data):
        self._id = str(data.get("_id"))
        self.email= data.get("email")
        self.password = data.get("password")
        self.create_at = str(datetime.utcnow())

    def save_to_db(self):
        db.users.update_one(
            {"email": self.email},
            {
                "$set": {
                    "password": generate_password_hash(self.password),
                    "created_at": self.create_at,

                }
            },
            True
        )

    def update_in_db(self):
        fields = {
            "email": self.email,
            "password": generate_password_hash(self.password)
        }
        set_fields = {}
        for key, val in fields.items():
            if val:
                set_fields[key] = val

        return db.users.update_one(
            {"_id": ObjectId(self._id)},
            {"$set": set_fields},
            False)

    @classmethod
    def find_by_id(cls,_id):
        data = db.users.find_one({"_id": ObjectId(_id)})
        if data:
            return data
        return None

    @classmethod
    def delete_by_id(cls,_id):
        if db.users.delete_one({"_id": ObjectId(_id)}):
            return True
        return False

    @classmethod
    def find_by_email(cls, email):
        data = db.users.find_one({"email": email})
        if data:
            return data
        return None

