from datetime import datetime

import parsedatetime
from flask import Blueprint, render_template, request

from pub.exts.init_sqlalchemy import db
from pub.models.models_business import User, Author
from pub.utils.http_utils import table_api
from pub.utils.rights import authorize
from pub.utils.string_utils import protect_mobile
from pub.utils.validate import str_escape

member_bp = Blueprint('member', __name__, url_prefix='/admin/member')


@member_bp.route('/')
@authorize("admin:member:main")
def main():
    return render_template('member/main.html')


@member_bp.route('/data', methods=['GET'])
@authorize("admin:member:main")
def data():  # 获取
    # 获取请求参数
    username = str_escape(request.args.get("username"))
    nick_name = str_escape(request.args.get('nick_name'))
    user_sex = str_escape(request.args.get('user_sex'))
    is_author = str_escape(request.args.get('is_author'))

    start_date = str_escape(request.args.get('start_date'))
    end_date = str_escape(request.args.get('end_date'))
    calendar = parsedatetime.Calendar()

    # 查询参数构造
    filters = []
    if username:
        filters.append(User.username.ilike('%' + username + '%'))
    if nick_name:
        filters.append(User.nick_name.ilike('%' + nick_name + '%'))
    if user_sex:
        filters.append(User.user_sex == user_sex)
    if is_author == '1':
        filters.append(Author.id != None)
    elif is_author == '0':
        filters.append(Author.id == None)
    if start_date:
        time_structure_start_time, parse_status_start_time = calendar.parse(start_date)
        start_date = datetime(*time_structure_start_time[:6])
        filters.append(User.create_time >= start_date)
    if end_date:
        time_structure_end_time, parse_status_end_time = calendar.parse(end_date)
        end_date = datetime(*time_structure_end_time[:6])
        filters.append(User.create_time <= end_date)

    # orm查询
    users = db.session.query(
        User, Author
    ).outerjoin(
        Author, User.id == Author.user_id
    ).filter(*filters).layui_paginate()
    count = users.total

    # 返回api
    return table_api(
        data=[
            {
                'id': str(user.id),
                'username': protect_mobile(user.username),
                'nick_name': protect_mobile(user.nick_name) if user.nick_name == user.username else user.nick_name,
                'user_sex': user.user_sex_translation,
                'account_balance': user.account_balance,
                'is_author': '是' if author else '否',
                'create_time': user.create_time.strftime("%Y-%m-%d %H:%M:%S")
            } for user, author in users.items
        ], count=count)
