from flask import Blueprint, redirect, url_for

index_bp = Blueprint('Index', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    return redirect(url_for('admin.index'))
