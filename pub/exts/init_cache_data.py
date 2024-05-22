from flask import Flask

from pub.models.models_system import User as AdminUser, Role, Power, Dept, DictType


def load_cache(app: Flask):
    with app.app_context():
        DictType.load_dicts()
