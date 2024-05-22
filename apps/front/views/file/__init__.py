from flask import Blueprint, request, jsonify, current_app

from pub.exts.init_upload import photos
from pub.utils.http_utils import fail_api
from pub.utils.upload import get_uuid_filename

file = Blueprint('file', __name__, url_prefix='/file')


def register_file_views(app):
    app.register_blueprint(file)


def upload(photo, mime):
    filename = photos.save(photo, name=get_uuid_filename(photo))
    file_url = '/_uploads/photos/' + filename
    upload_url = current_app.config.get("UPLOADED_PHOTOS_DEST")
    return file_url


#   上传接口
@file.post('/picUpload')
def upload_api():
    if 'file' in request.files:
        photo = request.files['file']
        mime = request.files['file'].content_type

        file_url = upload(photo=photo, mime=mime)
        res = {
            "msg": "上传成功",
            "code": 0,
            "success": True,
            "data":
                {"src": file_url}
        }
        return jsonify(res)
    return fail_api()
