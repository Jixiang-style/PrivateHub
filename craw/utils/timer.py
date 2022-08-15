#!/usr/bin/env python

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: timer.py
@time: 2022/7/6 10:45
@desc:
"""
import os
import time
from multiprocessing import Pool

# 多核优化性能
CPU_COUNT = os.cpu_count()


class Timer:
    # 定义计时器
    def timer(func=None):
        def timer_in(*args, **kwargs):
            time_start = time.time()
            func(*args, **kwargs)
            time_end = time.time() - time_start
            print("此次任务一共耗时%.2f秒" % time_end)

        return timer_in
