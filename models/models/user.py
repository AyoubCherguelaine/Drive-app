from pydantic import BaseModel
from bson.objectid import ObjectId
from . import db


class UserPost(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserEmail(BaseModel):
    email: str


class Ids(BaseModel):
    ids: list


def to_dict(user: UserPost):
    return {
        "name": user.name,
        "email": user.email,
        "password": user.password,
    }


class User:
    def __init__(self, user_):
        if all(key in user_ for key in ["name", "email", "password"]):
            self.name = user_["name"]
            self.email = user_["email"]
            self.password = user_["password"]
            self.files = []
            self.id = str(user_.get("ObjectId"))

    def dictionary(self):
        dictionary = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "files": self.files,
        }
        if self.id is not None:
            dictionary["_id"] = self.id

        return dictionary

    def save(self):
        result = db.db.user.insert_one(self.dictionary())
        self.id = str(result.inserted_id)

    @staticmethod
    def add_file(id_, id_file):
        query = {"_id": ObjectId(id_)}
        update = {"$push": {"files": id_file}}
        result = db.db.user.update_one(query, update)
        return result.modified_count == 1

    @staticmethod
    def delete(id_):
        result = db.db.user.delete_one({"_id": ObjectId(id_)})
        return {"result": result.deleted_count == 1}

    @staticmethod
    def get_one(id_):
        result = db.db.user.find_one({"_id": ObjectId(id_)})
        if result:
            result["_id"] = str(result["_id"])
        return result

    @staticmethod
    def get_all(filter_=None):
        if filter_ and isinstance(filter_, UserPost):
            filter_dict = to_dict(filter_)
            filter_dict = {key: value for key, value in filter_dict.items() if value}
            result = db.db.user.find(filter_dict)
        else:
            result = db.db.user.find()

        li = list(result)
        for i in li:
            i["_id"] = str(i["_id"])

        return li

    @staticmethod
    def is_file_allowed(id_user, id_file):
        user = User.get_one(id_user)
        return id_file in user.get("files", [])

    @staticmethod
    def authenticate(user_login):
        result = db.db.user.find_one({"email": user_login.email})
        if not result:
            return {"state": False}
        result["_id"] = str(result["_id"])
        if result["password"] == user_login.password:
            return {
                "state": True,
                "_id": result["_id"],
                "name": result["name"]
            }
        else:
            return {"state": False}

    @staticmethod
    def is_new_user(email):
        result = db.db.user.find_one({"email": email})
        return result is None

    @staticmethod
    def get_user(id_user):
        id_user = ObjectId(id_user)
        result = db.db.user.find_one({"_id": id_user})
        return result

    @staticmethod
    def get_users_by_ids(ids):
        projection = {'_id': 1, 'name': 1, 'email': 1}
        object_ids = [ObjectId(id_) for id_ in ids]
        users = db.db.user.find({'_id': {'$in': object_ids}}, projection)
        return list(users)
