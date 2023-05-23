from fastapi import FastAPI
from pydantic import BaseModel
# from models import files
# from models.files import file,filePost

from fastapi.middleware.cors import CORSMiddleware

from routes.file import router as fileRouter
from routes.user import router as userRouter

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Adjust with the actual origin of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fileRouter,prefix="/file",
    tags=["file"],
)

app.include_router(userRouter,prefix="/user",
    tags=["user"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,  port=8000)

