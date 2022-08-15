#!/usr/bin/env python

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: log.py
@time: 2022/7/7 14:25
@desc:
"""
import logging

logging.basicConfig(
    filename='craw.log',
    level=logging.INFO,
    filemode='a+',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%y-%m-%d %H:%M:%S '
)
