from flask import Blueprint, render_template

from pub.exts.init_sqlalchemy import db
from pub.models.models_business import UserFeedback, User
from pub.utils.http_utils import table_api
from pub.utils.rights import authorize

member_feedback_bp = Blueprint('member_feedback', __name__, url_prefix='/admin/member_feedback')


@member_feedback_bp.route('/')
@authorize("admin:member_feedback:main")
def main():
    return render_template('member/feedback.html')


@member_feedback_bp.route('/data', methods=['GET'])
@authorize("admin:member_feedback:main")
def data():  # 获取
    query_data = db.session.query(
        UserFeedback, User
    ).join(
        User, UserFeedback.user_id == User.id
    ).layui_paginate()
    # 返回api

    return table_api(
        data=
        [
            {
                'username': user.username,
                'content': user_feedback.content,
                'create_time': user_feedback.create_time
            } for user_feedback, user in query_data.items
        ], count=query_data.total)
