from fastapi import FastAPI, File, UploadFile, Depends
import os
from datetime import datetime
from manager import download, drb
from pydantic import BaseModel


app = FastAPI()

# Define an endpoint that requires authentication and handles file uploads
def get_upload_dir():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, "public", "upload")

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

# fin midell
@app.post("/upload/{UserPath}")
async def upload_file(UserPath:str,file: UploadFile = File(...)):
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Create the new filename with the timestamp
    filename, ext = os.path.splitext(file.filename)
    new_filename = f"{filename}_{timestamp}{ext}"
    
    # Save the file to disk
    
    upload_dir = get_upload_dir()+'/'+UserPath
    create_folder_if_not_exists(upload_dir)
    print(upload_dir,new_filename)
    with open(os.path.join(upload_dir, new_filename), "wb") as f:
        f.write(await file.read())
    
    return {"path":os.path.join(upload_dir, new_filename)}


class pathPost(BaseModel):
    path:str

@app.post("/download/")
async def download_file(path:pathPost):
    return download.download_file()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,  port=4003)


