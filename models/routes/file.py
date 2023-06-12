from fastapi import APIRouter

from models import files
from models.files import File, FilePost
from models.user import User, Ids

router = APIRouter()


@router.post("/create")
async def create_file(file_post: FilePost):
    print(file_post)
    file_dict = files.to_dict(file_post)
    f = File(file_dict)
    print(f.dictionary())
    ret= f.save()
    print(ret)
    return ret


@router.get("/")
async def get_all_files():
    return File.get_all(None)


@router.post("/")
async def get_files(filter: FilePost):
    return File.get_all(filter)


@router.get("/{id}/delete")
async def delete_file(id: str):
    return File.delete(id)


@router.get('/isFileAllow/{id_user}/{id_file}')
async def is_file_allow(id_user: str, id_file: str):
    return User.isFileAllow(id_user, id_file)


@router.get('/fileinfo/{id}')
async def file_info(id: str):
    file_info = File.get_one(id)
    users = File.get_user_in_file(id)
    return {
        "file": file_info,
        "users": users
    }


@router.post("/ids")
async def get_files_by_Ids(Ids: Ids):
    print(type(Ids.ids))
    
    return File.get_files_by_ids(Ids)
