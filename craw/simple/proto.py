#!/usr/local/bin/python3

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: proto.py
@time: 2022/7/12 10:57
@desc:
"""
import asyncio
import json
import re
import time
import sys, os
import random

import urllib3
from ffmpy3 import FFmpeg
import asyncio
import uvloop
from utils.timer import Timer
from utils.log import logging
from simple import FindNewWorld
import asyncio
import uvloop
from aiohttp import ClientSession
import time
from progressbar import *

sys.path.append(os.path.abspath(os.path.join(os.getcwd())).split('simple')[0])


def calculate():
    for i in range(50):
        print(f"我是第{i}个")


total = 100


def do_some_work():
    time.sleep(0.1)


widgets = [
    'Downloading: ',
    Percentage(), ' ',
    Bar('#'), ' ',
    Timer(), ' ',
    ETA(), ' ',
    FileTransferSpeed()
]


# bar = ProgressBar(widgets=widgets, maxval=10*total)
# for i in bar(range(total)):
#     do_some_work()

# from progress.bar import Bar
#
# bar = Bar("Loading", fill="#", max=100, suffix="%(percent)d%%")
# for i in bar.iter(range(total)):
#     do_some_work()

# for i in range(5):
#     t = threading.Thread(target=calculate)
#     t.start()

# t1 = time.time()
# time.sleep(1.6985544)
# t2 = time.time() - t1
# print("%.2f" % t2)
# FFmpeg(executable="/usr/local/bin/ffmpeg", inputs={"https://la.killcovid2021.com/m3u8/669611/669611.m3u8": None},
#        outputs={"少女穿着学校发的拉拉队衣服和我做爱完整版.mp4": None}).run()
# print(f"视频下载成功，耗时%.2f" % (time.time() - t1))

# 进度条测试
#
# from tqdm import tqdm, trange
#
# for i in tqdm(range(1000), desc="正在下载....."):
#     time.sleep(0.01)
#
# for i in trange(1000, desc="正在下载....."):
#     time.sleep(0.01)
def test_pool(num):
    for i in range(num):
        print(f"我是第{i}个")


async def sleep(n):
    print(f"我是第{n}个")
    time.sleep(n + 1)
    print(f"我是第{n}个，我醒啦")


task = list()


async def main(lists):
    for n in range(lists):
        task.append(asyncio.create_task(sleep(n)))
    print(task)
    return await asyncio.gather(*task)


time_1 = time.time()
lists = 5
loop = asyncio.get_event_loop()
# results = loop.run_until_complete(main(lists))
# print(results)
print("耗时", time.time() - time_1)

# async def main(n):
#     return await asyncio.gather(*[sleep(i) for i in range(n)])
#
# n = 5
# time_1 = time.time()
# results = asyncio.run(main(n))
# print(results)
# print("耗时", time.time() - time_1)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
urllib3.disable_warnings()
url = "https://www.baidu.com/"


def _download_by_ffmpeg():
    """
    通过ffmpeg下载视频
    :param m3u8_info:
    :type m3u8_info:
        m3u8_info : [dict] {title: m3u8_url}  视频基本信息，包括标题title，m3u8地址m3u8地址
    :param video_path:
    :type video_path:
        video_path : [str] 视频存放地址
    :return:
    :rtype:
    """
    # 整理json中保留的m3u8信息
    with open('./m3u8.json', 'r') as fp:
        info = json.load(fp)
    VIDEO_PATH = "./json_log/"
    raw_list = [v for item in info for k, v in item.items()]
    log_list = [i for i in raw_list if len(i) > 24][0]
    # 筛选出日志m3u8地址，并去重
    raw_list.remove(log_list)
    m3u8_infos = list(set(re.findall(r"https://la.*?[0-9].m3u8", str(raw_list))))
    for i in m3u8_infos:
        if i in log_list:
            log_list.remove(i)
    print(log_list)
    m3u8_info = dict()
    # 处理log文件中的地址
    for i in log_list:
        m3u8_info.update({str(random.randint(0, 1000)): i})
    # 处理每日日志中的地址
    for item in raw_list:
        if isinstance(item, list):
            for i in item:
                for k, v in i.items():
                    if v != "":
                        print(v)
                        expect_m3u8 = re.findall(r'https://la.*?[0-9].m3u8', str(v))[0]
                        if k != "" and expect_m3u8 != "":
                            m3u8_info.update({k: expect_m3u8})
                        elif k == "" and expect_m3u8 != "":
                            m3u8_info.update({str(random.randint(1000, 2000)): expect_m3u8})
        elif isinstance(item, dict):
            for k, v in item.items():
                if v != "":
                    print(v)
                    expect_m3u8 = re.findall(r'https://la.*?[0-9].m3u8', str(v))[0]
                    if k != "" and expect_m3u8 != "":
                        m3u8_info.update({k: expect_m3u8})
                    elif k == "" and expect_m3u8 != "":
                        m3u8_info.update({str(random.randint(2000, 3000)): expect_m3u8})
                # else:
                #     break
    print(m3u8_info)
    videos = os.listdir(VIDEO_PATH)
    for m3u8 in m3u8_info:
        for k, v in m3u8:
            tittle = 'list(i.keys())[0]'
            m3u8_url = 'list(i.values())[0]'
            video_name = "{}.mp4".format(tittle)
            video_path = VIDEO_PATH + video_name
            if video_name in videos:
                logging.info(f"视频{video_name}已存在，无需重新下载")
                print(f"视频{video_name}已存在，无需重新下载")
                break

            FFmpeg(executable="/usr/local/bin/ffmpeg",
                   inputs={m3u8_url: None},
                   outputs={video_path: None}).run()
            logging.info(f"视频{video_name}已存在已下载完成！！！")
            print(f"视频{video_name}已存在已下载完成！！！")


# _download_by_ffmpeg()

# 方法二 通过ts 文件合并视频
def _get_video_by_ts_data():
    # 视频存放路径
    VIDEO_PATH = "./json_log/"
    TS_PATH = "./ts_data/2022-08-10"

    # 整理m3u8地址
    with open('./m3u8.json', 'r') as fp:
        info = json.load(fp)
    raw_list = [v for item in info for k, v in item.items()]
    log_list = [i for i in raw_list if len(i) > 24][0]
    # 筛选出日志m3u8地址，并去重
    raw_list.remove(log_list)
    m3u8_infos = list(set(re.findall(r"https://la.*?[0-9].m3u8", str(raw_list))))
    for i in m3u8_infos:
        if i in log_list:
            log_list.remove(i)
    m3u8_info = dict()
    # 处理craw.log文件中的地址
    for i in log_list:
        m3u8_info.update({str(random.randint(0, 1000)): i})
    # 处理每日日志中的地址
    for item in raw_list:
        if isinstance(item, list):
            for i in item:
                for k, v in i.items():
                    if v != "":
                        expect_m3u8 = re.findall(r'https://la.*?[0-9].m3u8', str(v))[0]
                        if k != "" and expect_m3u8 != "":
                            m3u8_info.update({k: expect_m3u8})
                        elif k == "" and expect_m3u8 != "":
                            m3u8_info.update({str(random.randint(1000, 2000)): expect_m3u8})
        elif isinstance(item, dict):
            for k, v in item.items():
                if v != "":
                    expect_m3u8 = re.findall(r'https://la.*?[0-9].m3u8', str(v))[0]
                    if k != "" and expect_m3u8 != "":
                        m3u8_info.update({k: expect_m3u8})
                    elif k == "" and expect_m3u8 != "":
                        m3u8_info.update({str(random.randint(2000, 3000)): expect_m3u8})

    # 构建文件名
    for k, v in m3u8_info.items():
        mark_name = v.split("/")[-1]
        name = k + "({})".format(mark_name)
        ts_path = f'{TS_PATH}/{name}'
        # 产看本地已经存在的文件
        files = os.listdir(TS_PATH)
        # 防止出现Connection reset异常
        try:
            # 筛选出有中文名称的视频（文件名大于5）
            if len(k) > 5:
                # 判断是否有重复的文件夹
                if name in files:
                    print(f"{name}已存在,检测ts数据资源中....")
                    FindNewWorld().get_ts_datas(m3u8_base_url=v, ts_path=ts_path)
                    print(f"{name}数据检测完成...")
                    continue
            else:
                # 检查唯一标识m3u8编码
                mark_list = [re.findall(r"\(.*?\)", file)[0][1:-1] for file in files]
                # 检查是否有重复
                if mark_name in mark_list:
                    # 检查本地已存在的ts文件是否完整
                    ts_path = [file for file in files if mark_name in file][0]
                    print(f"{ts_path}已存在,检测ts数据资源中....")
                    FindNewWorld().get_ts_datas(m3u8_base_url=v, ts_path=r"{}/{}".format(TS_PATH, ts_path))
                    print(f"{ts_path}数据检测完成...")
                    continue
            os.mkdir(f'{ts_path}')
            print(f"获取{k}({v})文件资源中.....")
            FindNewWorld().get_ts_datas(m3u8_base_url=v, ts_path=ts_path)
        except OSError:
            print("该视频{}({})已经被下架...".format(k, v))
            # continue


# todo 待处理key懒加载问题
def _get_keys_in_page():
    page_url = "https://0117.workarea2.live/index.php"
    from selenium import webdriver
    # 设置无痕模式
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_option)
    # 进入浏览器首页
    driver.get(page_url)
    # 处理懒加载问题
    js = 'window.scrollTo(0, document.body.scrollHeight)'
    driver.execute_script(js)
    # print(driver.page_source)
    keys = re.findall("viewkey=(.*?)&amp", driver.page_source)
    print(set(keys))
    print("\n")
    print(len(list(set(keys))))

# _get_video_by_ts_data()
# _get_keys_in_page()
