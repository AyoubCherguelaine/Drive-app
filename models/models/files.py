from pydantic import BaseModel
from bson.objectid import ObjectId
from . import db
from .user import User
class filePost(BaseModel):
    name: str
    path: str
    label: str
    language: str
    id_user:str

def to_dict(file:filePost):
    dictionary= {
            "name":file.name,
            "path":file.path,
            "label":file.label,
            "language":file.language,
            "id_user":file.id_user
        }
    return dictionary
    

class file:

    def __init__(self,file_):
        
        if "name" in list(file_.keys()) and "path" in list(file_.keys()) and "label" in list(file_.keys()) and "language" in list(file_.keys()) and "id_user" in list(file_.keys()):
            name, path, label, language, id_user = file_["name"],file_["path"],file_["label"],file_["language"], file_["id_user"]
            self.name=name
            self.path= path
            self.label=label
            self.language= language
            self.id_user = id_user
            if "ObjectId" in list(file_.keys()):
                self.id = file_["ObjectId"]
            else:
                self.id = None
            

    def dictionary(self):
        dictionary= {
            "name":self.name,
            "path":self.path,
            "label":self.label,
            "language":self.language,
            "id_user": self.id_user
        }
        if self.id != None:
            dictionary["_id"] = self.id

        return dictionary

    def save(self):
        result =db.db.file.insert_one(self.dictionary())
        id = str(result.inserted_id)
        self.id = id
        User.addFile(self.id_user, id)
        
    
    @staticmethod
    def delete(id):
        result = db.db.file.delete_one({"_id":ObjectId(id)})
        if str(result.deleted_count) == 1:
            return {"result":True}
        else:
            return {"result":False}

    @staticmethod
    def getOne(id:str):
        _id= ObjectId(id)
        result = db.db.file.find_one({"_id":_id})
        result["_id"] = str(result["_id"])
        
        return result
    
    @staticmethod
    def get_all(filter:None):
        result= None
        if filter != None and type(filter) == filePost:
            filter = to_dict(filter)
            # Delete key-value pairs with empty values
            filter2 = {key: value for key, value in filter.items() if value != ""}
            result = db.db.file.find(filter2)
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
    def getUserInFile(idFile:str):
        
        cursor = db.db.user.aggregate([{"$unwind":"$files"},{"$match":{"files":idFile}}])
        result  = list(cursor)
        keys_to_delete = ['email', 'password', 'files']
        file.delete_keys(result, keys_to_delete)
        
        return result
        
    @staticmethod
    def get_files_by_ids(ids):
        print(ids.ids)
        ids = ids.ids
        # Convert the given IDs to ObjectId type
        object_ids = [ObjectId(id) for id in ids]

        # Query the collection for users with matching IDs
        users = db.db.file.find({'_id': {'$in': object_ids}})

        users_normalized = [user.update({'_id': str(user['_id'])}) or user for user in users]

        # Return the list of users
        return users_normalized


       