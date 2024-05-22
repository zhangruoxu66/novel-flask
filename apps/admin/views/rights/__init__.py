from flask import Flask

from .routes import rights_bp


def register_rights_view(app: Flask):
    app.register_blueprint(rights_bp)
