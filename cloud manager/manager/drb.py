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


def lag(text):
    l = text.split('/')

    return l[2]

def download_file(local_directory, dr_path):
    # Create a Dropbox client object using the access token


    try:
        # Download the file from Dropbox
        _, res = dbx.files_download(dr_path)
        data = res.content

        # Check if the local directory exists
        if not os.path.exists(local_directory):
            # Create the local directory
            os.makedirs(local_directory)

        # Get the filename from the Dropbox path
        filename = os.path.basename(lag(dr_path))

        # Construct the full local path
        local_path = os.path.join(local_directory, filename)

        # Write the downloaded data to the local file
        with open(local_path, "wb") as f:
            f.write(data)

        print("File downloaded from Dropbox:", local_path)
    except dropbox.exceptions.ApiError as e:
        print(f"Error downloading file from Dropbox: {e}")


