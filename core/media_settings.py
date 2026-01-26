from fastapi import UploadFile

async def save_image(image: UploadFile, path: str):
    image.file.seek(0)
    with open(path, "wb") as f:
        while chunk := image.file.read(1024 * 1024):
            f.write(chunk)

import os
PATH_TO_PROJECT = str(os.getenv("PATH_TO_PROJECT"))

def delete_image(path: str):
    full_path = os.path.join(PATH_TO_PROJECT, path)
    if os.path.exists(full_path):
        os.remove(full_path)