from flask import jsonify, request


def success_api(msg: str = "成功", code=0):
    """ 成功响应 默认值“成功” """
    return jsonify(success=True, code=code, msg=msg)


def fail_api(msg: str = "失败", code=9999):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, code=code, msg=msg)


def table_api(msg: str = "", count=0, data=None, limit: int = 10, page: int = 1):
    # if limit is None:
    #     limit = request.args.get('limit', type=int)
    # if page is None:
    #     page = request.args.get('page', type=int)
    """ 动态表格渲染响应 """
    res = {
        'msg': msg,
        'code': 0,
        'data': data,
        'count': count,
        'limit': limit,
        'page': page,
        'total_page': (count + limit - 1) // limit

    }
    return jsonify(res)


def is_ajax_request():
    requested_with = request.headers.get('X-Requested-With')
    if not requested_with:
        return False
    return 'XMLHttpRequest' == requested_with
