import os

from alipay import AliPay

env = "development"
if env == "production":
    # 支付宝应用APPID
    APP_ID = '20210021******'
    # 支付连接(支付宝网关)
    PAY_URL = 'https://openapi.alipay.com/gateway.do?'
else:
    # 沙箱
    APP_ID = os.environ.get('NOVEL_APP_ID')
    # PAY_URL = 'https://openapi.alipaydev.com/gateway.do?'
    PAY_URL = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?'

RSA_PRIVATE_KEY_BEGIN = '-----BEGIN RSA PRIVATE KEY-----\n'
RSA_PRIVATE_KEY_END = '\n-----END RSA PRIVATE KEY-----'
RSA_PUBLIC_KEY_BEGIN = '-----BEGIN PUBLIC KEY-----\n'
RSA_PUBLIC_KEY_END = '\n-----END PUBLIC KEY-----'
# 应用私钥文件路径
APP_PRIVATE_KEY = f"{RSA_PRIVATE_KEY_BEGIN}{os.environ.get('NOVEL_APP_PRIVATE_KEY')}{RSA_PRIVATE_KEY_END}"
# 支付宝公钥文件路径
ALIPAY_PUBLIC_KEY = f"{RSA_PUBLIC_KEY_BEGIN}{os.environ.get('NOVEL_ALIPAY_PUBLIC_KEY')}{RSA_PUBLIC_KEY_END}"
# 签名方式
SIGN_TYPE = 'RSA2'
# 是否是测试环境 - 是否是支付宝沙箱，默认为 False
DEBUG = True

# 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
NOTIFY_URL = "https://750c4868f6.goho.co/alipay/notify"
RETURN_URL = "http://127.0.0.1:8080/user/userinfo.html"


def alipay_trade_page_pay(pay_id, pay_amount, subject):
    alipay = AliPay(
        appid=APP_ID,
        app_notify_url=NOTIFY_URL,
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type=SIGN_TYPE,
        debug=DEBUG
    )

    # 生成支付链接
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=pay_id,
        total_amount=pay_amount,
        subject=subject,
        return_url=RETURN_URL,  # 支付成功后同步回调的项目前台页面
        notify_url=NOTIFY_URL  # 支付成功后异步回调的项目后台接口
    )

    # 支付链接 = 支付宝网关 +  order_string
    order_url = PAY_URL + order_string
    return order_url


# 验证支付结果
def verify_payment_result(data, signature):
    alipay = AliPay(
        appid=APP_ID,
        app_notify_url=None,
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type=SIGN_TYPE,
        debug=DEBUG
    )
    success = alipay.verify(data, signature)
    return success
