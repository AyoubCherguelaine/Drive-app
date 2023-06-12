from pydantic import BaseModel
from bson.objectid import ObjectId
from . import db
from .user import User


class FilePost(BaseModel):
    name: str
    path: str
    label: str
    language: str
    id_user: str


def to_dict(file: FilePost):
    dictionary = {
        "name": file.name,
        "path": file.path,
        "label": file.label,
        "language": file.language,
        "id_user": file.id_user
    }
    return dictionary


class File:

    def __init__(self, file_):
        if all(key in file_ for key in ["name", "path", "label", "language", "id_user"]):
            self.name = file_["name"]
            self.path = file_["path"]
            self.label = file_["label"]
            self.language = file_["language"]
            self.id_user = file_["id_user"]
            self.id=None
            

    def dictionary(self):
        dictionary = {
            "name": self.name,
            "path": self.path,
            "label": self.label,
            "language": self.language,
            "id_user": self.id_user
        }
        if self.id is not None:
            dictionary["_id"] = self.id

        return dictionary
    
    @staticmethod
    def dictionary_Base_model(obj):
        dictionary = {
            "name": obj.name,
            "path": obj.path,
            "label": obj.label,
            "language": obj.language,
            "id_user": obj.id_user
        }
        return dictionary

    def save(self):
        result = db.db.file.insert_one(self.dictionary())
        id_ = str(result.inserted_id)
        self.id = id_
        User.add_file(self.id_user, id_)
        return {
            "name": self.name,
            "path": self.path,
            "label": self.label,
            "language": self.language,
            "id_user": self.id_user,
            "_id" : id_
        }

    @staticmethod
    def delete(id_):
        result = db.db.file.delete_one({"_id": ObjectId(id_)})
        return {"result": result.deleted_count == 1}

    @staticmethod
    def get_one(id_):
        result = db.db.file.find_one({"_id": ObjectId(id_)})
        if result:
            result["_id"] = str(result["_id"])
        return result

    @staticmethod
    def get_all(filter_=None):
        if filter_ and isinstance(filter_, FilePost):
            filter_dict = to_dict(filter_)
            filter_dict = {key: value for key, value in filter_dict.items() if value}
            result = db.db.file.find(filter_dict)
        else:
            result = db.db.file.find()

        li = list(result)
        for i in li:
            i["_id"] = str(i["_id"])

        return li

    @staticmethod
    def delete_keys(data_list, keys):
        for data in data_list:
            data["_id"] = str(data["_id"])
            for key in keys:
                data.pop(key, None)

    @staticmethod
    def get_user_in_file(id_file):
        cursor = db.db.user.aggregate([{"$unwind": "$files"}, {"$match": {"files": id_file}}])
        result = list(cursor)
        keys_to_delete = ['email', 'password', 'files']
        File.delete_keys(result, keys_to_delete)
        return result

    @staticmethod
    def get_files_by_ids(ids):
        
        ids = ids.ids
        object_ids = [ObjectId(id_) for id_ in ids]
        users = db.db.file.find({'_id': {'$in': object_ids}})
        users_normalized = [user.update({'_id': str(user['_id'])}) or user for user in users]
        return users_normalized
