from flask import Blueprint, render_template, request

from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import News
from pub.utils.http_utils import success_api, table_api
from pub.utils.validate import str_escape

news_bp = Blueprint('news', __name__)


def register_news_views(app):
    app.register_blueprint(news_bp)


@news_bp.get('/about/newsInfo-<int:news_id>.html')
def news_info(news_id: int):
    news_obj = News.query.get(news_id)
    return render_template('about/news_info.html', news=news_obj)


@news_bp.get('/about/news.html')
def news():
    return render_template('about/news.html')


@news_bp.post('/news/addReadCount')
def add_read_count():
    req_json = request.get_json(force=True)
    news_id = str_escape(req_json.get("newsId"))

    news_obj = News.query.get(news_id)
    news_obj.read_count += 1
    db.session.add(news_obj)
    db.session.commit()

    return success_api()


@news_bp.get('/news/listByPage')
def list_by_page():
    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 5

    data = db.session.query(
        News.id, News.cat_id, News.cat_name, News.title, News.create_time
    ).order_by(
        News.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(data=AutoModelTransfer.model_2_dict(model=News, data=data.items), count=data.total,
                     limit=limit, page=page)
