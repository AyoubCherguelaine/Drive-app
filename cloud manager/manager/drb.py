import dropbox
import os
from . import config


# Access token for Dropbox API v2
access_token = config.access_token

dbx = dropbox.Dropbox(access_token)


async def upload_file(local_path,dr_path):
    """Uploads a file to Dropbox."""
    # Upload the file to Dropbox
    with open(local_path, 'rb') as f:
        file_name = os.path.basename(local_path)
        response = dbx.files_upload(f.read(), dr_path + '/' + file_name)

    return  response.path_display


def download_file(local_path,dr_path):
    # Path to the file you want to download from Dropbox
    # Download the file from Dropbox
    _, res = dbx.files_download(dropbox_path)
    data = res.content
    with open(local_path, "wb") as f:
        f.write(data)

    print("File downloaded from Dropbox: ", local_path)

