import inspect


def blind_copy(obj_from: object, obj_to: object):
    print(inspect.getmembers(obj_from))
    for n, v in inspect.getmembers(obj_from):
        setattr(obj_to, n, v)


def copy_some(obj_from: object, obj_to: object, names):
    for n in names:
        if hasattr(obj_from, n):
            v = getattr(obj_from, n)
            setattr(obj_to, n, v)
