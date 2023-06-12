from fastapi import APIRouter
from models import user
from models.user import User, UserPost, UserLogin, UserEmail

router = APIRouter()


@router.post("/create")
async def create_user(user_post: UserPost):
    user_dict = user.to_dict(user_post)
    user_obj = User(user_dict)
    user_obj.save()
    return user_obj.dictionary()


@router.get("/{id}")
async def get_user(id: str):
    return User.get_one(id)


@router.post("/ids")
async def get_users(ids: user.Ids):
    return User.get_users_by_ids(ids)


@router.get("/{id}/share/{id_file}")
async def share_file(id: str, id_file: str):
    return User.add_file(id, id_file)


@router.get("/")
async def get_all():
    return User.get_all(None)


@router.post("/")
async def get_users_filtered(filter: UserPost):
    return User.get_all(filter)


@router.get("/{id}/delete")
async def delete_user(id: str):
    return User.delete(id)


@router.post("/login")
async def login(body: UserLogin):
    print("call login")
    return User.auth(body)


@router.post("/isnewuser")
async def is_new_user(body: UserEmail):
    print("access")
    return User.is_new_user(body.email)
