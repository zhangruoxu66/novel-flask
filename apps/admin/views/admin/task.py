from datetime import datetime as dt

from flask import Blueprint, request, render_template
from flask_apscheduler.utils import job_to_dict

from pub.exts.init_apscheduler import scheduler
from pub.tasks import tasks
from pub.tasks.tasks import task_list
from pub.utils.http_utils import table_api, fail_api, success_api

admin_task = Blueprint('adminTask', __name__, url_prefix='/admin/task')


@admin_task.route('/add_job', methods=['GET'])
def add_task():
    scheduler.add_job(func=tasks.get(), id='4', args=(1, 1), trigger='interval', seconds=3,
                      replace_existing=True)
    return '6'


@admin_task.get('/')
def main():
    return render_template('admin/task/main.html')


@admin_task.route('/data', methods=['GET'])
def get_task():  # 获取
    jobs = scheduler.get_jobs()
    jobs_list = []
    for job in jobs:
        jobs_list.append(job_to_dict(job))
    return table_api(data=jobs_list, count=len(jobs_list))


# 增加
@admin_task.get('/add')
def add():
    return render_template('admin/task/add.html', task_list=task_list)


@admin_task.post('/save')
def save():
    _id = request.get_json(force=True).get("id")
    name = request.get_json(force=True).get("id")
    type = request.get_json(force=True).get("type")
    functions = request.get_json(force=True).get("functions")
    datetime = request.get_json(force=True).get("datetime")
    time = request.get_json(force=True).get("time")
    if not hasattr(tasks, functions):
        return fail_api()
    if type == 'date':
        scheduler.add_job(
            func=getattr(tasks, functions),
            id=_id,
            name=name,
            args=(1, 1),
            trigger=type,
            run_date=datetime,
            replace_existing=True)
    elif type == 'interval':
        # load time
        time = dt.strptime(time, "%H:%M:%S").time()
        interval_seconds = 0
        if time.hour != 0:
            interval_seconds += time.hour * 60 * 60
        if time.minute != 0:
            interval_seconds += time.minute * 60
        if time.second != 0:
            interval_seconds += time.second
        scheduler.add_job(
            func=getattr(tasks, functions),
            id=_id,
            name=name,
            args=(1, 1),
            trigger=type,
            seconds=interval_seconds,
            replace_existing=True)
    elif type == 'cron':
        scheduler.add_job(
            func=getattr(tasks, functions),
            id=_id,
            name=name,
            args=(1, 1),
            trigger=type,
            replace_existing=True)
    return success_api()


# 恢复
@admin_task.put('/enable')
def enable():
    _id = request.get_json(force=True).get('id')
    # print(id)
    if _id:
        scheduler.resume_job(str(_id))
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 暂停
@admin_task.put('/disable')
def dis_enable():
    _id = request.get_json(force=True).get('id')
    if _id:
        scheduler.pause_job(str(_id))
        return success_api(msg="暂停成功")
    return fail_api(msg="数据错误")


@admin_task.delete('/remove/<string:_id>/')
def remove_job(_id):  # 移除
    scheduler.remove_job(_id)
    return success_api(msg="删除成功")

    #     scheduler.add_job(func=task1, id='2', args=(1, 1), trigger='cron', day_of_week='0-6', hour=18, minute=24,
    #                       second=10, replace_existing=True)

    #     scheduler.add_job(func=task4, id='4', args=(2, 2), trigger='interval', seconds=3,
    #                       replace_existing=True, misfire_grace_time=3)

    #     # trigger='interval' 表示是一个循环任务，每隔多久执行一次
    #     scheduler.add_job(func=task2, id='3', args=(2, 2), trigger='interval', seconds=3,
    #                       replace_existing=True)
