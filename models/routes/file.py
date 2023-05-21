from fastapi import APIRouter
from models import files
from models.files import file,filePost
from models.user import User, ids

router = APIRouter()

@router.post("/create")
async def createFile(filePost:filePost):
    d_f = files.to_dict(filePost)
    
    f = file(d_f)
    
    f.save()
    return f.dictionary()

@router.get("/")
async def getAll():
    return file.get_all(None)

@router.post("/")
async def getAll(filter:filePost):
    return file.get_all(filter)

@router.get("/{id}/delete")
async def deleteFile(id:str):
    return file.delete(id)


@router.get('/isFileAllow/{id_user}/{id_file}')
async def isFileAllow(id_user:str,id_file:str):
    return User.isFileAllow(id_user, id_file)

@router.get('/fileinfo/{id}')
async def fileInfo(id:str):
    fileInfo = file.getOne(id)
    users = file.getUserInFile((id))
    return {
        "file":fileInfo,
        "users":users
    }
    
@router.post("/ids")
async def filesIds(ids:ids):
    return file.get_files_by_ids(ids)