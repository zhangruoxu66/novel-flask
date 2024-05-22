from flask import request


def get_real_ip():
    # 这个一般是Nginx反向代理设置的参数
    ip = request.headers.get('X-Real-IP')

    if not ip or len(ip) == 0 or 'unknown' == ip.lower():
        ip = request.headers.get('X-Forwarded-For')
    if not ip or len(ip) == 0 or 'unknown' == ip.lower():
        ip = request.headers.get('Proxy-Client-IP')
    if not ip or len(ip) == 0 or 'unknown' == ip.lower():
        ip = request.headers.get('WL-Proxy-Client-IP')
    if not ip or len(ip) == 0 or 'unknown' == ip.lower():
        ip = request.remote_addr

    # 处理多IP的情况（只取第一个IP）
    if ip and ',' in ip:
        ip = ip.split(',')[0]

    return ip
