from fastapi import FastAPI, File, UploadFile, Depends
import os
from datetime import datetime
from manager import download, drb

app = FastAPI()

# Define an endpoint that requires authentication and handles file uploads

def get_upload_dir():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, "public", "upload")



# fin midell
@app.post("/upload/{UserPath}")
async def upload_file(UserPath:str,file: UploadFile = File(...)):
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Create the new filename with the timestamp
    filename, ext = os.path.splitext(file.filename)
    new_filename = f"{filename}_{timestamp}{ext}"
    print(new_filename)
    # Save the file to disk
    upload_dir = get_upload_dir()
    with open(os.path.join(upload_dir, new_filename), "wb") as f:
        f.write(await file.read())
    print("greaat new_filename")

    # Upload the file to Dropbox
    dr_path = "/"+UserPath  # Set the desired Dropbox folder path

    dropbox_response = await drb.upload_file('./public/upload/'+new_filename, dr_path)
    
    print(dropbox_response)

    return {"filename": new_filename,"dr_path":dr_path}




@app.get("/download")
async def download_file():
    return download.download_file()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,  port=4001)


