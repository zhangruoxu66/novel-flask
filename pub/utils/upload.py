import os
import uuid

from flask import current_app
from sqlalchemy import desc
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from pub.curd import model_to_dicts
from pub.exts.init_sqlalchemy import db
from pub.exts.init_upload import photos
from pub.models.models_system import Photo
from pub.schemas.schemas_system import PhotoOutSchema


def get_photo(page, limit):
    photo = Photo.query.order_by(desc(Photo.create_time)).paginate(page=page, per_page=limit, error_out=False)
    count = Photo.query.count()
    data = model_to_dicts(schema=PhotoOutSchema, data=photo.items)
    return data, count


def get_uuid_filename(photo: FileStorage):
    extension_name = secure_filename(photo.filename).split('.')[-1]
    return f'{uuid.uuid4().hex}.{extension_name}'


def upload_one(photo: FileStorage, mime):
    filename = photos.save(photo, name=get_uuid_filename(photo))
    file_url = '/_uploads/photos/' + filename
    # file_url = photos.url(filename)
    upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
    size = os.path.getsize(upload_url + '/' + filename)
    photo = Photo(name=filename, href=file_url, mime=mime, size=size)
    db.session.add(photo)
    db.session.commit()
    return file_url


def delete_photo_by_id(_id):
    photo_name = Photo.query.filter_by(id=_id).first().name
    photo = Photo.query.filter_by(id=_id).delete()
    db.session.commit()
    upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
    try:
        os.remove(upload_url + '/' + photo_name)
    except FileNotFoundError:
        pass
    return photo
