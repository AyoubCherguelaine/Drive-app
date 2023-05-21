from pydantic import BaseModel
from bson.objectid import ObjectId
from . import db

class UserPost(BaseModel):
    name:str
    email:str
    password:str

class UserLogin(BaseModel):
    email:str
    password:str

class UserEmail(BaseModel):
    email:str

class ids(BaseModel):
    ids:list

def to_dict(user:UserPost):
    dictionary= {
            "name":user.name,
            "email":user.email,
            "password":user.password,
        }
    return dictionary

class User:
    def __init__(self,user_):
        if "name" in list(user_.keys()) and "email" in list(user_.keys()) and "password" in list(user_.keys()) :
            name,email,password = user_["name"],user_["email"],user_["password"]
            self.name = name
            self.email = email
            self.password = password
            self.files = []
            if "ObjectId" in list(user_.keys()):
                self.id = user_["ObjectId"]
            else:
                self.id = None
    

    def dictionary(self):
        dictionary= {
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "files":self.files
        }
        if self.id != None:
            dictionary["_id"] = self.id

        return dictionary
    
    def save(self):
        result =db.db.user.insert_one(self.dictionary())
        id = str(result.inserted_id)
        self.id = id

    @staticmethod
    def addFile(id,id_file):
        # Find the document where you want to append to the list
        query = {"_id": ObjectId(id)}

        # Update the document by appending to the list field
        update = {"$push": {"files": id_file }}
        result =db.db.user.update_one(query, update)
        if int(str(result.modified_count)) ==1 :
            return True
        else:
            return False
        

    @staticmethod
    def delete(id):
        result = db.db.user.delete_one({"_id":ObjectId(id)})
        if str(result.deleted_count) == 1:
            return {"result":True}
        else:
            return {"result":False}

    @staticmethod
    def getOne(id:str):
        _id= ObjectId(id)
        result = db.db.user.find_one({"_id":_id})
        result["_id"] = str(result["_id"])
       
        return result

    @staticmethod
    def get_all(filter:None):

        result= None
        if filter != None and type(filter) == filePost:
            filter = to_dict(filter)
            # Delete key-value pairs with empty values
            filter2 = {key: value for key, value in filter.items() if value != ""}
            result = db.db.user.find(filter2)
        else:
            result = db.db.user.find()
        li = list(result)
        for i in li:
            i["_id"] = str(i["_id"])
        
        return li

    @staticmethod
    def isFileAllow(id_User:str,id_File:str):
        user = User.getOne(id_User)
        if id_File in user["files"]:
            return True
        else:
            return False

    @staticmethod
    def Auth(UserPost:UserLogin):
        result = db.db.user.find_one({"email":UserPost.email})
        print(result)
        if result == None:
            return {"state":False}
        result["_id"] = str(result["_id"])
        if result["password"] == UserPost.password:
            return {"stat":True,
                    "_id":result["_id"],
                    "name":result["name"]
            }
        else:
            return {"state":False}

    @staticmethod
    def isNewUser(email:str):
        result = db.db.user.find_one({"email":email})
        if result == None:
            return True
        else:
            return False

    @staticmethod
    def getUser(id_user:str):
        id_user = ObjectId((id_user))
        result = db.db.user.find_one({"_id":id_user})
        return result

    @staticmethod
    def get_users_by_ids(ids):
        projection = {'_id': 1, 'name': 1,'email':1} 
        # Convert the given IDs to ObjectId type
        object_ids = [ObjectId(id) for id in ids]

    # Query the collection for users with matching IDs
        users = db.db.user.find({'_id': {'$in': object_ids}},projection)

    # Return the list of users
        return list(users)
