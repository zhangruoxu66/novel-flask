from flask import Blueprint, render_template, request, jsonify

from core.flask_redis_token.frt_utils import FRTUtils
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import NewsCategory
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_news_category_bp = Blueprint('admin_news_category', __name__, url_prefix='/admin/news_category')


@admin_news_category_bp.get('/')
@authorize("admin:news_category:main")
def main():
    return render_template('news_category/main.html')


@admin_news_category_bp.get('/data')
@authorize("admin:news_category:main")
def data():
    # orm查询
    page_data = db.session.query(
        NewsCategory
    ).order_by(NewsCategory.id.desc()).layui_paginate()
    count = page_data.total
    # 返回api
    return table_api(data=AutoModelTransfer.model_2_dict(page_data.items, NewsCategory), count=count)


@admin_news_category_bp.get('/add')
@authorize("admin:news_category:add", log=True)
def add():
    return render_template('news_category/add.html')


@admin_news_category_bp.post('/save')
@authorize("admin:news_category:add", log=True)
def save():
    req_json = request.get_json(force=True)
    name = str_escape(req_json.get('name'))
    sort = str_escape(req_json.get('sort'))

    nc = NewsCategory(name=name, sort=sort, create_user_id=FRTUtils.get_current_user().id,
                      update_user_id=FRTUtils.get_current_user().id)
    db.session.add(nc)
    db.session.commit()

    return success_api()


@admin_news_category_bp.get('/edit')
@authorize("admin:news_category:edit", log=True)
def edit():
    return render_template('news_category/edit.html')


@admin_news_category_bp.put('/update')
@authorize("admin:news_category:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id_ = str_escape(req_json.get('id'))
    name = str_escape(req_json.get('name'))
    sort = str_escape(req_json.get('sort'))

    NewsCategory.query.filter_by(id=id_).update({'name': name, 'sort': sort})
    db.session.commit()

    return success_api(msg="更新成功")


@admin_news_category_bp.get('/get_detail')
@authorize("admin:news_category:detail")
def get_detail():
    id_ = request.args.get("id")
    obj = NewsCategory.query.get(id_)
    res = {
        'id': obj.id,
        'name': obj.name,
        'sort': obj.sort
    }
    return jsonify(code=0, data=res)


@admin_news_category_bp.delete('/remove')
@authorize("admin:news_category:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = NewsCategory.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


@admin_news_category_bp.get('/all')
def load_all():
    list_data = NewsCategory.query.all()
    return jsonify(code=0, success=True, data=AutoModelTransfer.model_2_dict(data=list_data, model=NewsCategory))
