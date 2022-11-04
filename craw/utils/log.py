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
import logging.handlers

BASE_ERROR_PATH = './logs/errors/'
BASE_INFO_PATH = './logs/infos/'
# todo 处理结构化日志（分类处理）
logging.basicConfig(
    filename='craw.log',
    level=logging.INFO,
    filemode='a+',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%y-%m-%d %H:%M:%S '
)
logger = logging.getLogger(__name__)


# 根据日志类型写进不同的日志文件
# 处理全部日志
def _info():
    rf_handler = logging.handlers.RotatingFileHandler(f'{BASE_INFO_PATH}all.log', maxBytes=1024 * 1024 * 2,
                                                      backupCount=10)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s  [%(levelname)s]  %(message)s"))
    return rf_handler


# 处理错误日志
def _error():
    f_handler = logging.handlers.RotatingFileHandler(f'{BASE_ERROR_PATH}error.log', maxBytes=1024 * 1024 * 2,
                                                     backupCount=10)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s  [%(levelname)s]  %(filename)s[:%(lineno)d]  %(message)s"))
    return f_handler


logger.addHandler(_info())
logger.addHandler(_error())
# logger.addHandler(_file_logger())

# logger.debug('debug->10')
# logger.info('info->20')
# logger.warning('warning->30')
# logger.debug('debug->10')
# logger.error('error->40')
# logger.debug('debug->50')
# logger.info('info->60')
# logger.warning('warning->70')
# logger.debug('debug->80')
# logger.error('error->90')
