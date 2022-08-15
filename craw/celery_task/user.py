#!/usr/bin/env python

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: user.py
@time: 2022/7/12 15:11
@desc:
"""
import time

from tasks import find_study_video, find_dy_video, find_picture, send_mail, find_title
from tasks import app

# 设置时区
app.conf.timezone = 'Asia/Shanghai'

# 添加延迟任务，返回结果，任务号
from datetime import datetime, timedelta

# time_1 = datetime.utcnow() + timedelta(10)  # 十秒后执行
# t2_id = send_mail.delay()  # 返回任务号

# 添加定时任务，需要启动定时任务beat服务
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    # "study-video-task": {
    #     "task": "tasks.find_study_video",
    #     "schedule": timedelta(seconds=3),
    #     # "schedule": crontab(hour=8)
    #     "args": (20, 10)
    # },
    # "dy-video-task": {
    #     "task": "tasks.find_dy_video",
    #     "schedule": timedelta(seconds=3),
    #     # "schedule": crontab(hour=8)
    #     "args": (20, 10)
    #
    # },
    # "picture-task": {
    #     "task": "tasks.find_picture",
    #     "schedule": timedelta(seconds=3),
    #     # "schedule": crontab(hour=8)
    #     "args": (20, 10)
    # },
    "title-task": {
        "task": "tasks.find_title",
        "schedule": timedelta(seconds=3),
        # "schedule": crontab(hour=8)
        "args": (20, 10)
    },
}

# 启动命令： celery -A tasks worker --loglevel=info

