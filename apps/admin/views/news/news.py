from flask import Blueprint, render_template, request, jsonify

from core.flask_redis_token.frt_utils import FRTUtils
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import News
from pub.utils.http_utils import fail_api, success_api, table_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_news_bp = Blueprint('admin_news', __name__, url_prefix='/admin/news')


@admin_news_bp.get('/')
@authorize("admin:news:main")
def main():
    return render_template('news/main.html')


@admin_news_bp.get('/data')
@authorize("admin:news:main")
def data():
    # orm查询
    page_data = db.session.query(
        News
    ).order_by(News.id.desc()).layui_paginate()
    count = page_data.total
    # 返回api
    return table_api(data=AutoModelTransfer.model_2_dict(page_data.items, News), count=count)


@admin_news_bp.get('/add')
@authorize("admin:news:add", log=True)
def add():
    return render_template('news/add.html')


@admin_news_bp.post('/save')
@authorize("admin:news:add", log=True)
def save():
    req_json = request.get_json(force=True)
    cat_id = str_escape(req_json.get('cat_id'))
    cat_name = str_escape(req_json.get('cat_name'))
    source_name = str_escape(req_json.get('source_name'))
    title = str_escape(req_json.get('title'))
    content = req_json.get('content')

    news = News(cat_id=cat_id, cat_name=cat_name, source_name=source_name, title=title, content=content,
                create_user_id=FRTUtils.get_current_user().id, update_user_id=FRTUtils.get_current_user().id)
    db.session.add(news)
    db.session.commit()

    return success_api()


@admin_news_bp.get('/edit')
@authorize("admin:news:edit", log=True)
def edit():
    return render_template('news/edit.html')


@admin_news_bp.put('/update')
@authorize("admin:news:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id_ = str_escape(req_json.get('id'))
    cat_id = str_escape(req_json.get('cat_id'))
    cat_name = str_escape(req_json.get('cat_name'))
    source_name = str_escape(req_json.get('source_name'))
    title = str_escape(req_json.get('title'))
    content = req_json.get('content')

    News.query.filter_by(id=id_).update({
        'cat_id': cat_id,
        'cat_name': cat_name,
        'source_name': source_name,
        'title': title,
        'content': content,
    })
    db.session.commit()

    return success_api(msg="更新成功")


@admin_news_bp.get('/get_detail')
@authorize("admin:news:detail")
def get_detail():
    id_ = request.args.get("id")
    obj = News.query.get(id_)
    return jsonify(code=0, data=AutoModelTransfer.model_2_dict(obj, model=News, many=False))


@admin_news_bp.delete('/remove')
@authorize("admin:news:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = News.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")
