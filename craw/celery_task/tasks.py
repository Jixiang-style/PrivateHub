#!/usr/bin/env python

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: tasks.py
@time: 2022/7/12 15:10
@desc:
"""
import os

from celery import Celery
# from simple.simple import FindNewWorld
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd())).split('celery_task')[0])
from simple.simple import FindNewWorld
from dingtalkchatbot.chatbot import DingtalkChatbot

app = Celery('tasks', broker="redis://localhost:6379/0")


@app.task
def find_study_video():
    pass
    return "success"


@app.task
def find_dy_video():
    pass
    return "success"


@app.task
def find_title():
    # 开始爬取文本
    FindNewWorld.find_title()
    return "success"


@app.task
def find_picture():
    # 开始爬取图片
    FindNewWorld.find_picture()
    return "success"


@app.task
def send_mail(message):
    # 设置webhook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' \
              'bb9517fb7edb07f68f0010aaf20ba8fb807ac2e436d76f858fcd1812b51d53fb'
    # 初始化机器人
    xiaoding = DingtalkChatbot(webhook)
    # text消息推送
    message = "爬虫小助手craw提醒：" + message
    xiaoding.send_text(msg=message)
    # return "success"
# send_mail("测试成功")
