import os,secrets
from PIL import Image
from app import app

def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,"static/profile_pics",picture_fn)

    image = Image.open(form_picture)
    image.thumbnail((500,500))
    image.save(picture_path)

    return picture_fn

def delete_photo(form_picture):
    os.remove(os.path.join(app.root_path,"static/profile_pics",form_picture)) 