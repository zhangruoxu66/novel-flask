class DictConsts:
    YES_OR_NO = 'YES_OR_NO'
    SEX = 'SEX'
    book_rec_type = 'book_rec_type'
    work_direction = 'work_direction'  # 小说创作方向
    book_status = 'book_status'
    book_is_vip = 'book_is_vip'
    book_order_by_type = 'book_order_by_type'  # 小说排序方式
    is_enable = 'is_enable'  # 是否启用
    audit_status = 'audit_status'  # 审核状态
    pay_status = 'pay_status'  # 支付状态
    author_status = 'author_status'  # 作家状态

    class PayStatus:
        pay_status_success = 1  # 充值失败
        pay_status_fail = 0
        pay_status_wait = 2  # 待支付
