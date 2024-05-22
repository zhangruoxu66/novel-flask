# 渲染配置
import copy
from collections import OrderedDict

from flask import jsonify, current_app, Blueprint

from core.flask_redis_token.frt_utils import login_required, FRTUtils

from pub.models.models_system import Power
from pub.schemas.schemas_system import PowerOutSchema

rights_bp = Blueprint('rights', __name__, url_prefix='/rights')


@rights_bp.get('/configs')
@login_required
def configs():
    # 网站配置
    config = dict(logo={
        # 网站名称
        "title": current_app.config.get("SYSTEM_NAME"),
        # 网站图标
        "image": "/static/admin/admin/images/logo.png"
        # 菜单配置
    }, menu={
        # 菜单数据来源
        "data": "/rights/menu",
        "collaspe": False,
        # 是否同时只打开一个菜单目录
        "accordion": True,
        "method": "GET",
        # 是否开启多系统菜单模式
        "control": False,
        # 顶部菜单宽度 PX
        "controlWidth": 500,
        # 默认选中的菜单项
        "select": "0",
        # 是否开启异步菜单，false 时 data 属性设置为菜单数据，false 时为 json 文件或后端接口
        "async": True
    }, tab={
        # 是否开启多选项卡
        "enable": True,
        # 切换选项卡时，是否刷新页面状态
        "keepState": True,
        # 是否开启 Tab 记忆
        "session": True,
        # 最大可打开的选项卡数量
        "max": 30,
        "index": {
            # 标识 ID , 建议与菜单项中的 ID 一致
            "id": "10",
            # 页面地址
            "href": "/admin/welcome",
            # 标题
            "title": "首页"
        }
    }, theme={
        # 默认主题色，对应 colors 配置中的 ID 标识
        "defaultColor": "2",
        # 默认的菜单主题 dark-theme 黑 / light-theme 白
        "defaultMenu": "dark-theme",
        # 是否允许用户切换主题，false 时关闭自定义主题面板
        "allowCustom": True
    }, colors=[{
        "id": "1",
        "color": "#2d8cf0"
    },
        {
            "id": "2",
            "color": "#5FB878"
        },
        {
            "id": "3",
            "color": "#1E9FFF"
        }, {
            "id": "4",
            "color": "#FFB800"
        }, {
            "id": "5",
            "color": "darkgray"
        }
    ], links=current_app.config.get("SYSTEM_PANEL_LINKS"), other={
        # 主页动画时长
        "keepLoad": 1200,
        # 布局顶部主题
        "autoHead": False
    }, header=False)
    return jsonify(config)


# 菜单
@rights_bp.get('/menu')
@login_required
def menu():
    if FRTUtils.get_current_user().username != current_app.config.get("SUPERADMIN"):
        permissions = FRTUtils.get_session().get('permissions')
        power_dict = []
        # 遍历角色用户的权限
        for p in permissions:
            # 一二级菜单
            if int(p.type) in [0, 1] and p not in power_dict:
                power_dict.append(p)

        power_schema = PowerOutSchema(many=True)
        power_dict = power_schema.dump(power_dict)

        return get_menu_tree(power_dict)
    else:
        menus = Power.query.all()
        power_schema = PowerOutSchema(many=True)  # 用已继承 ma.ModelSchema 类的自定制类生成序列化类
        power_dict = power_schema.dump(menus)  # 生成可序列化对象

        return get_menu_tree(power_dict)


def get_menu_tree(power_dict):
    power_dict.sort(key=lambda x: (x['parent_id'], x['id']), reverse=True)

    menu_dict = OrderedDict()
    for _dict in power_dict:
        if _dict['id'] in menu_dict:
            # 当前节点添加子节点
            _dict['children'] = copy.deepcopy(menu_dict[_dict['id']])
            _dict['children'].sort(key=lambda item: item['sort'])
            # 删除子节点
            del menu_dict[_dict['id']]

        if _dict['parent_id'] not in menu_dict:
            menu_dict[_dict['parent_id']] = [_dict]
        else:
            menu_dict[_dict['parent_id']].append(_dict)
    return jsonify(sorted(menu_dict.get(0), key=lambda item: item['sort']))
