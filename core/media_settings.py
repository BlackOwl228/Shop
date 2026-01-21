def save_product_image(image_bytes: bytes, filename: str, product_id: int):

    img_path = os.path.join("media", "product", str(product_id))

    ext = filename.split('.')[-1]
    full_path = f"{img_path}.{ext}"

    with open(full_path, "wb") as f:
        f.write(image_bytes)


def save_avatar(image_bytes: bytes, filename: str, user_id: int):

    img_path = os.path.join("media", "avatar", str(user_id))

    ext = filename.split('.')[-1]
    full_path = f"{img_path}.{ext}"

    with open(full_path, "wb") as f:
        f.write(image_bytes)
        

import os
PATH_TO_PROJECT = str(os.getenv("PATH_TO_PROJECT"))

def delete_image(dir: str, filename: str):
    full_path = os.path.join(PATH_TO_PROJECT, "media", dir, filename)
    if os.path.exists(full_path):
        os.remove(full_path)