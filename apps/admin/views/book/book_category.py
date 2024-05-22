from flask import Blueprint, jsonify

from pub.curd import AutoModelTransfer
from pub.models.models_business import BookCategory

admin_book_category_bp = Blueprint('admin_book_category', __name__, url_prefix='/admin/book_category')


@admin_book_category_bp.get('/all')
def load_all():
    data = BookCategory.query.all()
    return jsonify(code=0, success=True, data=AutoModelTransfer.model_2_dict(data=data, model=BookCategory))
