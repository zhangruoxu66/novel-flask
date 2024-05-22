from flask import render_template, jsonify, redirect, url_for
from flask_siwadoc import ValidationError

from pub.utils.http_utils import is_ajax_request


def init_error_views(app):
    @app.errorhandler(401)
    def page_not_found(e):
        return redirect(url_for('passport.login')), 401

    @app.errorhandler(ValidationError)
    def validate_error(e: ValidationError):
        return jsonify({"success": False, 'code': -1, "msg": '请求参数错误'})

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        if is_ajax_request():
            return jsonify(success=False, code=9999, msg='不存在的资源！')
        else:
            return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."]).get('json')
        msg = ''

        for i in messages.items():
            msg = str(i[0]) + str(i[1][0])
            break

        if headers:
            return jsonify({"success": False, 'code': 9999, "msg": msg})
        else:
            return jsonify({"success": False, 'code': 9999, "msg": msg})
