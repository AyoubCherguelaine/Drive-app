
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import os


# Define a route to download a file

def download_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    file_path = script_dir+"/public/NLP cv.pdf"  # Replace with the path to your file
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]

    # Use the FileResponse class to send the file as a response
    return FileResponse(file_path, filename=file_name, media_type=f"application/{file_extension}")
