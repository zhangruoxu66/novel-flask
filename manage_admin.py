from apps.admin import create_app
from apps.admin.exts.init_websocket import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    # app.run()
