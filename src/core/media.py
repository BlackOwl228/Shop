import os
from fastapi import UploadFile

async def save_image(image: UploadFile, path: str):
    image.file.seek(0)
    with open(path, "wb") as f:
        while chunk := image.file.read(1024 * 1024):
            f.write(chunk)

def delete_image(path: str):
    full_path = os.path.join(os.getcwd(), path)
    if os.path.exists(full_path):
        os.remove(full_path)