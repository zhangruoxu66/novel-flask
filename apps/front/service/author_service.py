from sqlalchemy import text

from pub.exts.init_sqlalchemy import db
from pub.models.models_business import AuthorFollow


def get_follow_status_by_uid(author_id: int, user_id: int) -> int:
    """
    根据用户id获取是否关注作家

    :param author_id: 作家id
    :param user_id: 用户id

    :return: 0：未关注；1：已关注
    """
    count = AuthorFollow.query.filter(
        AuthorFollow.author_id == author_id,
        AuthorFollow.user_id == user_id
    ).count()

    return 1 if count > 0 else 0


def get_follow_status(author_id: int, identity) -> int:
    """
    获取作家关注状态

    :param author_id: 作家id
    :param identity: JWT身份认证信息

    :return: 0：未关注；1：已关注；2：未登录
    """
    if not identity or not identity.get('id'):
        return 2

    return get_follow_status_by_uid(author_id, identity.get('id'))


def add_author_visit_count_by_uid(author_id: int, user_id: int):
    """
    根据用户id增加**关注**作家的访问次数

    :param author_id: 作家id
    :param user_id: 用户id
    """
    # 未关注则不需要进行操作
    count = AuthorFollow.query.filter(
        AuthorFollow.author_id == author_id,
        AuthorFollow.user_id == user_id
    ).count()
    if count <= 0:
        return

    db.session.execute(text(
        f'update novel_flask.author_follow a '
        f'set a.visit_count = a.visit_count + 1 '
        f'where a.author_id = {author_id} and a.user_id = {user_id}'
    ))
    db.session.commit()


def add_author_visit_count(author_id: int, identity):
    """
    增加**关注**作家的访问次数

    :param author_id: 作家id
    :param identity: JWT身份认证信息
    """
    if not identity or not identity.get('id'):
        return
    add_author_visit_count_by_uid(author_id, identity.get('id'))
