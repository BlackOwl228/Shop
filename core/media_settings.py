from fastapi import UploadFile
async def save_product_image(image: UploadFile, product_id: int):
    img_path = os.path.join("media", "product", str(product_id))
    ext = image.filename.split('.')[-1]
    filename = f"{img_path}.{ext}"
    with open(filename, "wb") as file_object:
        while True:
            chunk = await image.read(1024)
            if not chunk:
                break
            file_object.write(chunk)

    return filename

async def save_avatar(image: UploadFile, user_id: int):
    img_path = os.path.join("media", "avatar", str(user_id))
    ext = image.filename.split('.')[-1]
    filename = f"{img_path}.{ext}"
    with open(filename, "wb") as file_object:
        while True:
            chunk = await image.read(1024)
            if not chunk:
                break
            file_object.write(chunk)

    return filename

import os
PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")

async def delete_image(dir: str, filename: str):
    full_path = os.path.join(PATH_TO_PROJECT, "media", dir, filename)
    if os.path.exists(full_path):
        await os.remove(full_path)
        return True
    return False