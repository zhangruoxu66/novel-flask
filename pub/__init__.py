from concurrent.futures import ThreadPoolExecutor

from flask import current_app

executor = ThreadPoolExecutor(4)


def context_wrap(fn):
    app_context = current_app.app_context()

    def wrapper(*args, **kwargs):
        with app_context:
            return fn(*args, **kwargs)

    return wrapper
