from flask import Flask
from flask_migrate import Migrate

from pub.exts.init_sqlalchemy import db

migrate = Migrate()


def init_migrate(app: Flask):
    migrate.init_app(app, db)
