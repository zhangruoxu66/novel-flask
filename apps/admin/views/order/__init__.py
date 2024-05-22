from flask import Blueprint, render_template, request

from pub.consts.dict_consts import DictConsts
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import OrderPay, User
from pub.models.models_system import DictType
from pub.utils import string_utils
from pub.utils.http_utils import table_api
from pub.utils.rights import authorize

order_bp = Blueprint('order', __name__, url_prefix='/admin/order')


def register_order_views(app):
    app.register_blueprint(order_bp)


@order_bp.get('/')
@authorize("admin:order:main")
def index():
    return render_template('order/main_new.html')


@order_bp.get('/data')
@authorize("admin:order:main")
def login_log():
    # 获取请求参数
    pay_status = request.args.get("pay_status", type=int)
    filters = []
    if pay_status is not None:
        filters.append(OrderPay.pay_status == pay_status)

    page_data = db.session.query(
        OrderPay.out_trade_no, OrderPay.total_amount, OrderPay.user_id, OrderPay.pay_status, OrderPay.create_time,
        User.username
    ).join(
        User, OrderPay.user_id == User.id
    ).filter(
        *filters
    ).order_by(OrderPay.create_time.desc()).layui_paginate()
    count = page_data.total

    res = [
        {
            'out_trade_no': data.out_trade_no,
            'total_amount': data.total_amount,
            'username': string_utils.protect_mobile(data.username),
            'pay_status': data.pay_status,
            'pay_status_name': DictType.translate(DictConsts.pay_status, data.pay_status),
            'create_time': data.create_time.strftime("%Y-%m-%d %H:%M:%S") if data.create_time else '',
        } for data in page_data.items
    ]

    return table_api(data=res, count=count)
