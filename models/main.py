from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from routes.file import router as fileRouter
from routes.user import router as userRouter

from  routes import file 

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Adjust with the actual origin of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file.router, prefix="/file", tags=["file"])
app.include_router(userRouter, prefix="/user", tags=["user"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
