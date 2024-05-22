import json
import random
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity

from apps.front.exts.init_jwt import user_login_req
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import OrderPay
from pub.utils.alipay_utils import alipay_trade_page_pay, verify_payment_result

alipay_bp = Blueprint('alipay', __name__, url_prefix='/alipay')


def register_alipay_views(app):
    app.register_blueprint(alipay_bp)


@alipay_bp.get('/index.html')
@user_login_req
def index():
    return render_template('pay/index.html')


@alipay_bp.post('/pay')
@user_login_req
def get_alipay():
    identity = get_jwt_identity()

    total_amount = request.form.get('payAmount')

    # 创建充值订单
    cur_date = datetime.now()
    out_trade_no = int(cur_date.strftime('%Y%m%d%H%M%S') + str(random.randrange(10)))
    order_pay = OrderPay(out_trade_no=out_trade_no, pay_channel=1, total_amount=total_amount,
                         user_id=identity.get('id'),
                         create_time=cur_date, update_time=cur_date)
    db.session.add(order_pay)
    db.session.commit()

    pay_url = alipay_trade_page_pay(
        pay_id=uuid.uuid4().hex,  # 用户购买的商品订单号
        pay_amount=total_amount,  # 交易金额
        subject='充值屋币'  # 商品描述
    )

    return jsonify(code=0, success=True, pay_url=pay_url)


@alipay_bp.post('/notify')
@user_login_req
def notify():
    data = request.form.to_dict()
    # sign must be poped out
    signature = data.pop("sign")
    print(json.dumps(data))
    print(signature)
    # verify
    success = verify_payment_result(data, signature)
    # 交易结果判断
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        # 商户订单号
        out_trade_no = data['out_trade_no']
        # 支付宝交易号
        trade_no = data['trade_no']
        # 支付宝交易号
        trade_status = data['trade_status']

        order_pay = OrderPay.query.filter_by(out_trade_no=out_trade_no).first()
        order_pay.trade_no = trade_no
        order_pay.pay_status = trade_status
        db.session.add(order_pay)
        db.session.commit()

        print("trade succeed")
        resp = jsonify(success=True, msg='支付成功')
    else:
        resp = jsonify(success=False, msg='支付失败')

    return resp
