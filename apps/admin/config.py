from pub.config import BaseConfig


class AdminConfig(BaseConfig):
    PORT = 5000

    SUPERADMIN = 'admin'

    SYSTEM_NAME = 'Pear Admin'
    # 主题面板的链接列表配置
    SYSTEM_PANEL_LINKS = [
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "官方网站",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开发文档",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开源地址",
            "href": "https://gitee.com/Jmysy/Pear-Admin-Layui"
        }
    ]

    SECRET_KEY = "pear-admin-flask"

    FLASK_REDIS_TOKEN_SESSION_COOKIE = False
    FLASK_REDIS_TOKEN_LOGIN_VIEW = 'passport.login'
    FLASK_REDIS_TOKEN_SUPER_ADMIN_ROLE = 'SUPER_ADMIN'
    FLASK_REDIS_TOKEN_REMEMBER_ME = False

    FLASK_REDIS_TOKEN_CSRF_PROTECT = True
    FLASK_REDIS_TOKEN_CSRF_IN_COOKIES = True
    FLASK_REDIS_TOKEN_CSRF_HEADER_NAME = "FLASK-CSRF-TOKEN"
    FLASK_REDIS_TOKEN_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
