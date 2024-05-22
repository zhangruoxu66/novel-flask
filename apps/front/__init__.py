import os

from flask import Flask

from apps.front.config import FrontConfig
from apps.front.exts import init_plugs
from apps.front.views import init_view


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')),
                template_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')))
    # 引入数据库配置
    app.config.from_object(FrontConfig)

    # 注册各种插件
    init_plugs(app)

    # 注册路由
    init_view(app)

    return app
