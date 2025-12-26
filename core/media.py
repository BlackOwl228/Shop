from fastapi import UploadFile
def save_product_image(image: UploadFile, product_id: int):
    img_path = os.path.join("product", str(product_id))
    ext = image.filename.split('.')[-1]
    filename = f"{img_path}.{ext}"
    with open(filename, "wb") as file_object:
        while True:
            chunk = image.read(1024)
            if not chunk:
                break
            file_object.write(chunk)

    return filename

def save_avatar(image: UploadFile, user_id: int):
    img_path = os.path.join("product", str(user_id))
    ext = image.filename.split('.')[-1]
    filename = f"{img_path}.{ext}"
    with open(filename, "wb") as file_object:
        while True:
            chunk = image.read(1024)
            if not chunk:
                break
            file_object.write(chunk)

    return filename

import os
PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")

def delete_image(dir: str, filename: str):
    full_path = os.path.join(PATH_TO_PROJECT, "media", dir, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
        return True
    return False