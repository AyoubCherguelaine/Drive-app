from fastapi import APIRouter
from models import user
from models.user import User,UserPost, UserLogin, UserEmail

router = APIRouter()

@router.post("/create")
async def createUser(UserPost:UserPost):
    
    d_u = user.to_dict(UserPost)
    
    U = User(d_u)
    
    U.save()
    return U.dictionary()

@router.get("/{id}")
async def getUser(id:str):
    return User.getOne(id)

@router.post("/ids")
async def getusers(ids:user.ids):
    return User.get_users_by_ids(ids)

@router.get("/{id}/share/{id_file}")
async def chareAfile(id:str,id_file:str):
    return User.addFile(id, id_file)
    

@router.get("/")
async def getAll():
    return User.get_all(None)

@router.post("/")
async def getAll(filter:UserPost):
    return User.get_all(filter)

@router.get("/{id}/delete")
async def deleteUser(id:str):
    return User.delete(id)

@router.get("/{id}")
async def getOne(id:str):
    return User.getOne(id)

@router.post("/login")
async def Login(body:UserLogin):
    print("call login")
    return User.Auth(body)

@router.post("/isnewuser")
async def isNewUser(body:UserEmail):
    print("access")
    return User.isNewUser(body.email)