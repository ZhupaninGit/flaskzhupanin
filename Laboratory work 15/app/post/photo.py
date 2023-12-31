import os,secrets
from PIL import Image
from flask import current_app

def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,"static/post_pics",picture_fn)
    print(form_picture)
    image = Image.open(form_picture)
    image.save(picture_path)

    return picture_fn


def delete_photo(form_picture):
    if form_picture == "default.jpg":
        return
    os.remove(os.path.join(current_app.root_path,"static/post_pics",form_picture)) 