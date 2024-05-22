import os
from flask import Flask

from apps.admin.common.script import init_script
from apps.admin.config import AdminConfig
from apps.admin.exts import init_plugs
from apps.admin.views import init_view


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')),
                template_folder=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')))
    # 引入数据库配置
    app.config.from_object(AdminConfig)

    # 注册各种插件
    init_plugs(app)

    # 注册路由
    init_view(app)

    # 注册命令
    init_script(app)

    print('启动成功')

    return app
