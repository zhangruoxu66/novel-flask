from flask import Flask, request
from flask_socketio import SocketIO, emit

socketio = SocketIO(async_mode='eventlet')

# 用来保存用户ID到会话ID的映射
user_to_sid = {}


@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    socketio.emit('response', {'data': 'Message received'})


# @socketio.on('connect')
# def handle_connect():
#     client_sid = request.sid
#     print(f"Client socket id: {client_sid}")


@socketio.on('register')
def handle_register(data):
    user_id = int(data['uid'])
    sid = request.sid  # 获取当前会话的ID

    # 保存用户ID到会话ID的映射
    user_to_sid[user_id] = sid
    print(user_to_sid)

    # 可以选择发送一个确认消息回客户端
    emit('registered', {'status': 'success'}, room=sid)


# 注意：这里我们使用装饰器参数sid来获取会话ID
@socketio.on('disconnect')
def handle_disconnect():
    # 当客户端断开连接时，从映射中移除其用户ID和会话ID
    sid = request.sid
    # 当客户端断开连接时，从映射中移除对应的用户ID
    for user_id, stored_sid in list(user_to_sid.items()):
        if stored_sid == sid:
            del user_to_sid[user_id]
            break


# 发送消息给特定用户的函数
def send_message_to_user(user_id: int, code: int, message):
    sid = user_to_sid.get(user_id)
    if sid:
        socketio.emit('server_message', {'code': code, 'data': message}, to=sid)
    else:
        print(f"User {user_id} is not connected.")


# 踢下线提醒
def kickout_notice(user_id: int):
    send_message_to_user(user_id, 5001, '您已被管理员踢下线！')
    del user_to_sid[user_id]


# 冻结提醒
def freeze_notice(user_id: int):
    send_message_to_user(user_id, 5002, '当前会话已被管理员冻结！')


def init_socketio(app: Flask):
    socketio.init_app(app)
