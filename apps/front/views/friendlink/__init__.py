from flask import Blueprint, jsonify

from pub.consts import RedisKey
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import FriendLink
from pub.utils.redis_utils import Redis

friend_link_bp = Blueprint('friend_link', __name__, url_prefix='/friendLink')


def register_friend_link_views(app):
    app.register_blueprint(friend_link_bp)


def get_data():
    data = Redis.get(RedisKey.INDEX_LINK_KEY, default=None)
    if data:
        data = AutoModelTransfer.json_2_dict(model=FriendLink, data=data)
        return data

    data = db.session.query(
        FriendLink.link_name, FriendLink.link_url
    ).filter(
        FriendLink.is_open == 1
    ).order_by(
        FriendLink.sort.asc()
    ).all()
    json_data = AutoModelTransfer.model_2_dict(model=FriendLink, data=data)
    Redis.set(RedisKey.INDEX_LINK_KEY, AutoModelTransfer.model_2_json(model=FriendLink, data=data))
    return json_data


@friend_link_bp.route('/listIndexLink')
def list_index_link():
    return jsonify(code=0, msg="", data=get_data())
