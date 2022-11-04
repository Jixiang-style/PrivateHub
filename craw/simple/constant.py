#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:craw
@file: contant.py
@author: 薛吉祥
@time: 2022/11/4 17:06
@desc:
"""
import os


class Constant(object):
    # 图片基础设置

    SCROLL_HIGH = 2000  # 屏幕像素点
    IMAGE_PATH = './picture/'
    EXIST_IMAGES = set(os.listdir(IMAGE_PATH))

    # 视频基础设置
    DY_VIDEO_PATH = './dy_video/'

    # 学习视频
    FUN_VIDEO_PATH = "./study_video/"
    FUN_TS_PATH = "./ts_data/"
    FUN_RETRY_VIDEO_PATH = "./retry_video/"
