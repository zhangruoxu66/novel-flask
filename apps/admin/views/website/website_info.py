from flask import Blueprint, render_template, request

from pub.exts.init_sqlalchemy import db
from pub.models.models_business import WebsiteInfo
from pub.utils.http_utils import success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_website_info_bp = Blueprint('admin_website_info', __name__, url_prefix='/admin/website_info')


@admin_website_info_bp.get('/')
@authorize("admin:website_info:main")
def main():
    data = WebsiteInfo.query.get(1)
    return render_template('website/main.html', websiteInfo=data)


@admin_website_info_bp.post('/update')
@authorize("admin:website_info:edit")
def edit():
    req_json = request.get_json(force=True)
    id = str_escape(req_json.get('id'))
    name = str_escape(req_json.get('name'))
    domain = str_escape(req_json.get('domain'))
    keyword = str_escape(req_json.get('keyword'))
    description = str_escape(req_json.get('description'))
    qq = str_escape(req_json.get('qq'))
    logo = str_escape(req_json.get('logo'))
    logoDark = str_escape(req_json.get('logoDark'))

    WebsiteInfo.query.filter_by(id=id).update({
        'name': name
        , 'domain': domain
        , 'keyword': keyword
        , 'description': description
        , 'qq': qq
        , 'logo': logo
        , 'logo_dark': logoDark
    })

    db.session.commit()

    return success_api()
