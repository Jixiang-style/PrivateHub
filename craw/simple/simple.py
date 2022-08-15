#!/usr/bin/env python

# encoding: utf-8
"""
@author: Xue JiXiang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: xuejixiang@forchange.tech
@software: pycharm
@file: simple.py
@time: 2022/7/5 17:15
@desc:
"""
import datetime
import os
import random
import re
import sys
import time
from io import BytesIO

import aiohttp
import asyncio

from PIL import Image
from tqdm import tqdm
import jsonpath
import m3u8
import pytesseract
import requests
import seldom

# 消除警告信息
import urllib3
import uvloop
from aiohttp import ClientSession, ClientRequest
from urllib.parse import unquote

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
urllib3.disable_warnings()

sys.path.append(os.path.abspath(os.path.join(os.getcwd())).split('simple')[0])
from utils.timer import Timer
from utils.log import logging

# 定义请求头
headers = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.0.0 Safari/537.36"
}


# 倒计时
def calculate_time(func=None, time_out=None, *args, **kwargs):
    """
    程序倒计时
    :param time_out:
    :type time_out:
    :return:
    :rtype:
    """
    if func is None:
        return "目标函数为空！！！"
    try:
        if isinstance(time_out, int):
            t1 = time.time()
            while True:
                stout = func(*args, **kwargs)
                if time.time() - t1 <= time_out:
                    pass
                else:
                    return False
    except TimeoutError as e:
        print("程序运行超时：", e.strerror)


# todo 该函数待优化
def wait_until(func=None, timeout=None, msg=None, *args, **kwargs):
    """
    超时等待
    :param func: [function] 目标函数
    :param timeout: [int] 超时时间
    :param msg: [str] 超时信息
    :return:
    """
    if func is None:
        print("target function is required")
        return

    if not isinstance(timeout, int):
        timeout = int(timeout)

    start_time = time.time()
    while True:
        res_time = time.time() - start_time
        if res_time > timeout:
            print(msg)
            raise TimeoutError
        try:
            param = kwargs.values()
            res = func(list(param)[0])
            if res:
                print(f"")
                return res
        except OSError:
            print("retrying...")


class FindNewWorld:

    @Timer.timer
    def find_html(self, url=None):
        # 1.简单爬取搜狗数据
        # 1.指定URL
        if url is None:
            url = "https://www.sogou.com/"
        # 2. 发送请求
        req = requests.get(url=url)
        # 3.获取数据
        data = req.text
        # 4.持久化存储
        with open("sogou.html", "w", encoding="UTF-8") as f:
            f.write(data)
        print(data)

    @Timer.timer
    def find_title(self, url=None):
        # 2.爬取豆瓣电影分类排行榜 https：//movie.douban.com/中电影详情
        # 1.指定URL
        url = "https://movie.douban.com/j/search_subjects"

        # 参数设置
        params = {
            "type": "movie",
            "tag": "战争",
            "page_limit": 100,
            "page_start": 0
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.0.0 Safari/537.36"
        }
        for i in range(50):
            params["page_start"] += 1
            req = requests.get(url=url, params=params, headers=headers)
            # print(req.text)

            for item in req.json()["subjects"]:
                with open("douban.text", "a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write(item["title"])
                    f.write("\n")
                    f.write(item["id"])
                    f.write("\n")
                    f.write(item["cover"])
                    f.write("\n")
                    f.write(item["url"])
                    f.write("\n")
                    f.close()

    @Timer.timer
    def find_picture(self, url=None, num=None):
        # 爬取图片(例如：https://www.pexels.com/zh-cn/)
        # 基础设置
        SCROLL_HIGH = 2000  # 屏幕像素点
        IMAGE_PATH = './picture/'
        EXIST_IMAGES = set(os.listdir(IMAGE_PATH))

        DOWNLOAD_LENGTH = num
        if num is None:
            DOWNLOAD_LENGTH = 100  # 设置下载图片数量
        # 1.指定URL
        if url is None:
            url = "https://www.pexels.com/"
        message = f"需要下载{num}图片"
        logging.info(message)

        browser = seldom.TestCase()
        # 隐藏window.navigator.webdriver 避免反爬机制，原博客：https://juejin.cn/post/6844904095749242887(该方法seldom已封装)
        # brower.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        # Object.defineProperty(navigator, 'webdriver', {
        #   get: () => undefined
        # })
        # """
        # })
        # 设置浏览器无头模式
        browser.open(url)
        elements = browser.get_elements(xpath="//article")
        # while len(elements) < DOWNLOAD_LENGTH:
        # 如果页面展示图片数目小于目标数目，执行js下滑到页面底部
        if len(elements) < DOWNLOAD_LENGTH:
            browser.execute_script('window.scrollTo(0, {})'.format(SCROLL_HIGH))
        for i in range(DOWNLOAD_LENGTH):
            path = browser.get_attribute(attribute="href", index=i,
                                         xpath="//article//ancestor::a[contains(@title,'下载')]")
            name = browser.get_attribute(attribute="alt", index=i, xpath="//article//ancestor::a//img")
            # title = f"./picture/{name}.jpg"
            name = "".join(re.findall(r'[\u4e00-\u9fa5]+', name))
            image = f"{name}.jpg"
            title = IMAGE_PATH + image
            if image in EXIST_IMAGES:
                logging.info(f"图片{image}已存在无需重新下载")
                break

            # 请求图片资源
            req = requests.get(url=path)
            if req.status_code != 200:
                logging.error(f"下载{image}失败！status_code:{req.status_code}")
                break
            with open(title, "ab+") as f:
                f.write(req.content)
                logging.info(f"下载{image}成功！URL：{path}")

    # todo 需完善
    @Timer.timer
    def find_dy_video(self, url=None):
        # 基础配置
        VIDEO_PATH = './dy_video/'

        # 1.指定URL
        # 随机码
        random_field = '00nvcRAUjgJQBMjqpgesfdNJ72&dytk=4a01c95562f1f10264fb14086512f919'
        # 网址的主体
        max_cursor = 0
        url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?' \
              'sec_uid=MS4wLjABAAAAU7Bwg8WznVaafqWLyLUwcVUf9LgrKGYmctJ3n5SwlOA&count=21&max_cursor=' + str(
            max_cursor) + '&aid=1128&_signature=' + random_field
        # 请求头
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit'
                          '/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 获取相应数据
            response = response.json()
            # 获取视频路径
            paths = response["aweme_list"]
            video_realurls = list()
            # 批量获取视频路径
            for path in paths:
                # 视频简介
                video_title = path['desc']
                # 获取视频地址（无水印地址）
                video_urls = jsonpath.jsonpath(path, '$..play_addr')[0]
                video_url = video_urls['url_list'][1]
                video = video_url, video_title
                video_realurls.append(video)
            # 获取视频数目
            numbers = response["max_cursor"]

            # 批量获取视频数据
            for item in video_realurls[:2]:
                # 2. 发送请求
                # 构建文件名
                name = "".join(re.findall(r'[\u4e00-\u9fa5]+', item[1]))
                name_dir = VIDEO_PATH + f"{name}.mp4"
                # 请求数据
                req = requests.get(url=item[0])
                start_time = time.time()
                if req.status_code == 200:
                    logging.info(f"开始下载{name}....")
                    # 持久化存储
                    with open(name_dir, "ab+") as f:
                        f.write(req.content)
                else:
                    logging.error(f"{name}下载失败....")
                logging.info("耗时%.2f秒，%s下载完成！！！" % (start_time - time.time(), name))
        else:
            logging.error(f"请求视频列表数据异常....")

    @Timer.timer
    def find_study_videos(self, flag):
        # 抓取91学习视频
        # 设置视频存放路径
        VIDEO_PATH = "./study_video/"
        TS_PATH = "./ts_data/"
        videos = os.listdir(VIDEO_PATH)
        # 如果连接访问不了，在这里把base_url替换成你知道的标准地址
        # base_url = 'http://f1020.workarea5.live/view_video.php?viewkey='
        base_url = 'https://0117.workarea2.live/view_video.php?viewkey='
        # page_url = 'http://f1020.workarea5.live/v.php?category=top&viewtype=basic&page=' + str(flag)
        # todo 该地址待改进，暂时换成首页地址
        # page_url = 'https://0117.workarea2.live/v.php?category=rf&viewtype=basic&page=' + str(flag)
        page_url = "https://0117.workarea2.live/index.php"

        # 定义随机ip地址
        def _random_ip():
            a = random.randint(1, 255)
            b = random.randint(1, 255)
            c = random.randint(1, 255)
            d = random.randint(1, 255)
            ip = (str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d))
            return ip

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36Name',
            'Referer': 'http://91porn.com'}
        header_single = {'Accept-Language': 'zh-CN,zh;q=0.9',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
                         'X-Forwarded-For': _random_ip(),
                         'referer': page_url,
                         'Content-Type': 'multipart/form-data; session_language=cn_CN',
                         'Connection': 'keep-alive',
                         'Upgrade-Insecure-Requests': '1',
                         }

        # 识别图片中的文本
        async def _image2strings(image_url):
            """
            识别图片上的文字（中英文）
            :param image_url:
                image_url: [str] 图片的线上地址
            :type image_url:
            :return:
            :rtype:
            """
            async with ClientSession() as session:
                async with session.get(image_url) as response:
                    status_code = response.status
                    if status_code == 200:
                        response = await response.read()
                        return response
                    else:
                        print("获取title图片失败")
                        return None

        # 处理日志m3u8地址
        def _handle_log():
            # 1.获取日志文件信息
            context = ""
            import json
            with open("./craw.log", mode="r", encoding="utf-8") as fp1:
                for i in fp1.readlines():
                    context += i
            print(context)
            # m3u8_paths = list()
            data = list(set(re.findall(r"https://.*.m3u8", context)))
            long_data = [i for i in data if len(i) > 60]
            for item in long_data:
                raw_items = item.split(",")
                # data.append([re.findall(r"https://.*.m3u8", i)[0] for i in raw_items if len(i) > 1 and
                #              len(re.findall(r"https://.*.m3u8", i)[0]) > 1])
                items = raw_items.pop()
                m3u8_url = re.findall(r"https://.*.m3u8", items)[0]
                data.append(m3u8_url)
                for i in raw_items:
                    if len(i) < 30:
                        break
                    else:
                        data.append(re.findall(r"https://.*.m3u8", i)[0])
            print(data)
            for i in list(set(data)):
                if len(i) > 80:
                    data.remove(i)
            print(data)
            data = list(set(data))

            # todo 把m3u8地址写进json文件
            time_title = datetime.date.today()
            with open("./m3u8.json", mode="r", encoding="utf-8") as fp1:
                old_data = json.load(fp1)
                # old_data.append({str(time_title): m3u8_infos[0]})
                # 把日志URL写进json文件
                old_data.append({str(time_title): data})
            with open("./m3u8.json", mode="w", encoding="utf-8") as fp2:
                # ensure_ascii=False设置防止中文乱码
                json.dump(old_data, fp2, ensure_ascii=False)

        _handle_log()

        # 拉丁文转换为utf-8
        def _latin2utf8(strings):
            # 拉丁文转为utf-8标砖字符，例如：\xe6\x9e\x81\  => 猴赛雷
            utf8_stings = strings.encode("latin1").decode("unicode_escape").encode('latin1').decode('utf8')
            return utf8_stings

        # 获取指定页面内（index）视频keys列表
        def _get_keys():
            try:
                get_page = requests.get(url=page_url, headers=headers, timeout=60, verify=False)
            except requests.exceptions.ConnectTimeout as e:
                logging.error(f"获取首页信息超时：{e.strerror}")
                print(f"获取首页信息超时：{e.strerror}")
                raise TimeoutError
            else:
                if get_page.status_code == 200:
                    # 利用正则匹配出特征地址
                    # view_keys = re.findall(r'viewkey=(.*?)&page', str(get_page.content))
                    # 更新获取方式（2022-08-11）
                    view_keys = re.findall(r'viewkey=(.*?)&', str(get_page.content))
                    # 去重
                    view_keys = list(set(view_keys))
                    logging.info(f"本次一共收集到{len(view_keys)}个学习视频...")
                    # 调试
                    print(f"本次一共收集到{len(view_keys)}个学习视频...")

                    for key in view_keys:
                        logging.info('find:' + key)
                        print('find:' + key)
                    return view_keys

                else:
                    logging.error(f"获取91首页内容失败，请检查91地址是否更新！")
                    print("获取91首页内容失败，请检查91地址是否更新！")

        # 异步获取首页视频的m3u8列表
        def _get_m3u8_urls_async(view_key_list):
            # view_keys = _get_keys()
            video_info = list()
            # 设置重试列表
            retry_key = list()
            print("开始获取中.....")

            async def main(keys):
                return await asyncio.gather(*[_get_m3u8_info_async(key) for key in keys])

            loop = asyncio.get_event_loop()
            m3u8_info = loop.run_until_complete(main(view_key_list))

            print(m3u8_info)
            # return m3u8_info
            for k, v in m3u8_info.items():
                if v[0] != "":
                    video_info.append(m3u8_info)
                else:
                    retry_key.append({k: v[1]})
            return video_info, retry_key

        # 普通获取首页视频的m3u8列表
        def _get_m3u8_urls(view_key_list):
            video_info = list()
            # 设置重试列表
            retry_key = list()
            print("开始获取中.....")

            for key in view_key_list:
                # 获取m3u8信息
                print(f"正在获取key为{key}的m3u8地址...")
                logging.info(f"正在获取key为{key}的m3u8地址...")
                m3u8_info = _get_m3u8_info(key)
                print(m3u8_info)
                for k, v in m3u8_info.items():
                    if v[0] != "":
                        video_info.append(m3u8_info)
                    else:
                        retry_key.append({k: v[1]})
            return video_info, retry_key

        # 获取单个key获取的m3u8信息（普通方法）
        def _get_m3u8_info(key):
            base_req = requests.get(url=base_url + key, headers=header_single, timeout=60, verify=False)
            base_req.encoding = base_req.apparent_encoding
            from urllib.parse import unquote
            if base_req.status_code == 200:
                # 获取视频名称
                raw_title = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>',
                                       str(base_req.content), re.S)[0]
                raw_title = sorted(raw_title.split(" "), key=lambda x: len(x), reverse=True)[0]
                """
                 \xe6\x9e\x81\xe5\x93\x81\xe9\x98\xbf\xe5\xa7\xa8\xef\xbc\x8c\xe8\xba\xab\xe6\x9d\x90\xe8\x8b\x97\xe6\
                 x9d\xa1\xe5\x85\xb3\xe9\x94\xae\xe5\xa5\xb6\xe5\xad\x90\xe8\xbf\x99\xe4\xb9\x88\xe6\x8c\xba\xe6\x8b\x94\n
                """
                tittle = _latin2utf8(raw_title).strip("\n").strip(" ")
                if "http" in tittle:
                    title_png_url = re.findall(r'https://.*.png', tittle)[0]
                    # 91视频文字更新为图片
                    # (todo bug待处理)方法一 ：用easyocr库识别
                    # 创建reader对象
                    # reader = easyocr.Reader(['ch_sim', 'en'])
                    # 读取图片
                    # https://title.t6k.co/img_title/7f578lLiov5HGy99uLJr6JAGt42Wl9T3TL4tFRSDfwAqnaM.png
                    # result = reader.readtext(title_png_url)
                    # 方法二： 使用tesseract处理
                    from PIL import Image
                    im = Image.open(BytesIO(requests.get(url=title_png_url).content))
                    tittle = pytesseract.image_to_string(im, lang='chi_sim+eng')

                # 匹配中文
                tittle = re.findall(r'[\u4e00-\u9fa5]+', tittle)
                if isinstance(tittle, list):
                    tittle = "".join(tittle)

                # 获取视频内容
                str_encode = re.findall(r'strencode2\(\"(.*?)\"\)', str(base_req.content))
                m3u8_base_url = ""
                if len(str_encode) >= 1:
                    logging.info(f"m3u8地址为{unquote(str_encode[0])}")
                    print(f"key为{key}对应的m3u8地址为{unquote(str_encode[0])}")
                    m3u8_base_url = re.findall(r'src=(.*?) type', unquote(str_encode[0]))[0][1:-1]
                else:
                    logging.info(f"首次获取{key}对应的m3u8地址失败，正在重新获取...")
                    print(f"首次获取{key}对应的m3u8地址失败，正在重新获取...")
                single_info = dict()
                single_info[tittle] = m3u8_base_url, key
                return single_info
            else:
                logging.error(f"获取key:{key}视频内容信息失败!")
                print(f"获取key: {key}视频内容信息失败!")

        # 异步获取单个key获取的m3u8信息 (todo 待优化)
        async def _get_m3u8_info_async(key):
            time_out = aiohttp.ClientTimeout(total=120)
            async with ClientSession(headers=header_single, timeout=time_out) as session:
                async with session.get(url=base_url + key, headers=header_single, timeout=time_out) as response:
                    status_code = response.status
                    print("status", response.status)
                    response = await response.read()
                    print(response)
                    if status_code == 200:
                        # 获取视频名称
                        raw_title = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>',
                                               str(response), re.S)[0]
                        raw_title = sorted(raw_title.split(" "), key=lambda x: len(x), reverse=True)[0]
                        tittle = _latin2utf8(raw_title).strip("\n").strip(" ")
                        if "http" in tittle:
                            title_png_url = re.findall(r'https://.*.png', tittle)[0]
                            # 91视频文字更新为图片
                            # (todo bug待处理)方法一 ：用easyocr库识别
                            # 创建reader对象
                            # reader = easyocr.Reader(['ch_sim', 'en'])
                            # 读取图片
                            # https://title.t6k.co/img_title/7f578lLiov5HGy99uLJr6JAGt42Wl9T3TL4tFRSDfwAqnaM.png
                            # result = reader.readtext(title_png_url)

                            # 方法二： 使用tesseract处理(异步处理)
                            loop = asyncio.get_event_loop()
                            im = loop.run_until_complete(_image2strings(title_png_url))
                            # im = Image.open(BytesIO(requests.get(url=title_png_url).content))
                            if im:
                                tittle = pytesseract.image_to_string(im, lang='chi_sim+eng')

                        # 匹配中文
                        tittle = re.findall(r'[\u4e00-\u9fa5]+', tittle)
                        if isinstance(tittle, list):
                            tittle = "".join(tittle)

                        # 获取视频内容
                        str_encode = re.findall(r'strencode2\(\"(.*?)\"\)', str(response))
                        m3u8_base_url = ""
                        if len(str_encode) >= 1:
                            logging.info(f"m3u8地址为{unquote(str_encode[0])}")
                            print(f"key为{key}对应的m3u8地址为{unquote(str_encode[0])}")
                            m3u8_base_url = re.findall(r'src=(.*?) type', unquote(str_encode[0]))[0][1:-1]
                        else:
                            logging.info(f"首次获取{key}对应的m3u8地址失败，正在重新获取...")
                            print(f"首次获取{key}对应的m3u8地址失败，正在重新获取...")

                        single_info = dict()
                        single_info[tittle] = m3u8_base_url, key
                        print(single_info)
                        return single_info
                    else:
                        logging.error(f"获取key:{key}视频内容信息失败!")
                        print(f"获取key: {key}视频内容信息失败!")

        # 获取视频信息
        def _get_video_info(key):
            base_req = requests.get(url=base_url + key, headers=header_single, timeout=60, verify=False)
            # todo 待完善
            if base_req.status_code == 200:
                # 获取视频名称
                raw_title = re.findall(r'<h4 class="login_register_header" align=left>(.*?)</h4>',
                                       str(base_req.content), re.S)[0]
                raw_title = sorted(raw_title.split(" "), key=lambda x: len(x), reverse=True)[0]
                """
                 \xe6\x9e\x81\xe5\x93\x81\xe9\x98\xbf\xe5\xa7\xa8\xef\xbc\x8c\xe8\xba\xab\xe6\x9d\x90\xe8\x8b\x97\xe6\
                 x9d\xa1\xe5\x85\xb3\xe9\x94\xae\xe5\xa5\xb6\xe5\xad\x90\xe8\xbf\x99\xe4\xb9\x88\xe6\x8c\xba\xe6\x8b\x94\n
                """
                tittle = _latin2utf8(raw_title).strip("\n").strip(" ")
                # 匹配中文
                tittle = re.findall(r'[\u4e00-\u9fa5]+', tittle)
                if isinstance(tittle, list):
                    tittle = "".join(tittle)
                # 获取视频封面
                img_url = re.findall(r'poster="(.*?)"',
                                     str(base_req.content))  # 'https://img.91p51.com/thumb/667137.jpg'
                return tittle, img_url

        # 获取视频片段ts数据
        def _get_ts_data(url, time_out):
            ts_data = requests.get(url=url, timeout=time_out, verify=False)
            return ts_data

        # 下载视频
        def _download(m3u8_base_url, tittle):
            m3u8_obj = m3u8.load(m3u8_base_url)
            m3u8_urls = [m3u8_obj.base_uri + ts for ts in m3u8_obj.files]
            # 设置视频路径待处理
            video_name = "{}.mp4".format(tittle)
            video_path = VIDEO_PATH + video_name
            if video_name in videos:
                logging.info(f"视频{video_name}已存在，无需重新下载")
                print(f"视频{video_name}已存在，无需重新下载")
            # 开始拼接ts视频
            logging.info(f"开始下载{tittle}....")
            # 调试
            print(f"开始下载{tittle}....")
            time_start = time.time()
            # 进度条展示
            from progressbar import ProgressBar, Percentage, Bar, Timer, ETA, FileTransferSpeed
            widgets = [
                'Downloading: ',
                Percentage(), ' ',
                Bar('#'), ' ',
                Timer(), ' ',
                ETA(), ' ',
                FileTransferSpeed()
            ]
            bar = ProgressBar(widgets=widgets, maxval=10 * len(m3u8_urls))
            print(f"该视频解析出{len(m3u8_urls)}个ts文件")
            logging.info(f"该视频解析出{len(m3u8_urls)}个ts文件")
            # 设置ts文件顺序
            index = 0
            for url in bar(m3u8_urls):
                try:
                    ts_data = _get_ts_data(url=url, time_out=120)
                    logging.info("正在获取第{}个ts文件....".format(index))
                    print("正在获取第{}个ts文件....".format(index))
                except TimeoutError as e:
                    logging.error("获取第{}个ts数据异常".format(index))
                    print("获取第{}个ts数据异常".format(index))
                    break
                else:
                    if ts_data.status_code == 200:
                        with open(video_path, "ab+") as fp:
                            fp.write(ts_data.content)
                    else:
                        logging.info(f"下载{tittle}的ts数据时状态请求异常....")
                        print(f"下载{tittle}时状态请求异常....")
                index += 1
            logging.info("耗时%.2f秒，%s下载完成！！！" % (time.time() - time_start, tittle))
            print("耗时%.2f秒，%s下载完成！！！" % (time.time() - time_start, tittle))
            """
            'https://la.killcovid2021.com/m3u8/667838/'
            """

        # 方法一
        # 通过ffmpeg下载视频（todo 待优化）
        def _download_by_ffmpeg(m3u8_info, video_path):
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
            for i in m3u8_info:
                tittle = list(i.keys())[0]
                m3u8_url = list(i.values())[0]
                video_name = "{}.mp4".format(tittle)
                video_path = VIDEO_PATH + video_name
                if video_name in videos:
                    logging.info(f"视频{video_name}已存在，无需重新下载")
                    print(f"视频{video_name}已存在，无需重新下载")
                    break
                from ffmpy3 import FFmpeg
                FFmpeg(executable="/usr/local/bin/ffmpeg",
                       inputs={m3u8_url: None},
                       outputs={video_path: None}).run()
                logging.info(f"视频{video_name}已存在已下载完成！！！")
                print(f"视频{video_name}已存在已下载完成！！！")

        # 设置视频序号
        # # todo 剩余未能成功获取的m3u8地址原因未找到
        # # retry_key_list = [list(i.values()).pop() for i in m3u8_infos[1]]
        # # 通过视频对应的key下载指定视频
        # # for key in retry_key_list:
        # #     # 获取m3u8信息
        # #     m3u8_info = _get_m3u8_info(key)
        # #
        # #     # 根据key获取视频信息
        # #     # title, img_url = _get_video_info(key)
        # #     #
        # #     # # 获取m3u8地址
        # #     # m3u8_url = _get_m3u8_url(key)
        # #     # for k, v in m3u8_infos[0]:
        # #     #     if v == "":
        # #     #         retry_keys.append(m3u8_info["key"])
        # #     # video_info.append({m3u8_info})
        # #     # 方法一（不稳定）
        # #     # 开始下载
        # #     # logging.info(f"准备下载第{video_index}个视频\n 视频加密地址为{m3u8_info.values()}")
        # #     # _download(m3u8_url, title)
        # #     print(m3u8_info)
        # #     video_index += 1
        # print(video_info)
        # # todo 将m3u8新纪录写进json文件
        # for item in video_info:
        #     if len(list(item.values())) < 1:
        #         video_info.remove(item)

        # 处理当天最新逻辑
        # 1.获取key列表
        key_list = _get_keys()

        # 2.获取m3u8信息列表
        # m3u8_list = list()
        # todo 待调试
        # async def m3u8_main(key_list):
        #     return await asyncio.gather(*[_get_m3u8_info_async(key) for key in key_list])
        #
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(m3u8_main(key_list))
        # m3u8_list = _get_m3u8_urls_async(key_list)
        # 2.1 普通方法获取
        m3u8_list = list()
        for i in key_list:
            j = _get_m3u8_info(i)
            m3u8_list.append(j)
        print("m3u8_list", m3u8_list)
        m3u8_list = [i for i in m3u8_list if i is not None and list(i.values())[0][0] != ""]
        print("一共获取到%d个地址" % len(m3u8_list))
        # 3 获取ts文件
        # 3.1 创建当日文件夹（文件名为当前日期）
        dir_name = time.strftime("%Y-%m-%d", time.localtime())
        dirs = os.listdir(TS_PATH)
        if dir_name not in dirs:
            os.makedirs(f"{TS_PATH}{dir_name}")
        ts_base_path = TS_PATH + dir_name
        exist_dirs = os.listdir(ts_base_path)
        for item in m3u8_list:
            m3u8_url = list(item.values())[0][0]
            title = list(item.keys())[0]
            m3u8_mark = m3u8_url.split("/")[-1]
            file = f"{title}({m3u8_mark})"
            ts_path = f"{ts_base_path}/{file}"
            # 防止出现Connection reset异常
            try:
                if file in exist_dirs:
                    print(f"{file}已存在,检测ts数据资源中....")
                    FindNewWorld().get_ts_datas(m3u8_base_url=m3u8_url, ts_path=ts_path)
                    print(f"{file}数据检测完成...")
                    continue
                os.mkdir(f'{ts_path}')
                print(f"获取{file}文件资源中.....")
                FindNewWorld().get_ts_datas(m3u8_base_url=m3u8_url, ts_path=ts_path)
            except OSError:
                print("该视频{}已经被下架...".format(file))

        # 根据m3u8列表获取ts文件待优化
        # async def main(url_list, ts_path):
        #     return await asyncio.gather(
        #         *[_get_ts_data(url) for url in tqdm(url_list, desc="Downloading: ") if
        #           url.split("/")[-1] not in os.listdir(ts_path)])
        #
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(m3u8_urls, ts_path))
        # self.get_ts_datas()
        # print(len(m3u8_list))
        # 3.获取ts数据列表

    @Timer.timer
    def find_single_study_video(self, url, tittle):
        # url 需要为m3u8_url
        # 设置视频存放路径
        VIDEO_PATH = "./retry_video/"
        videos = os.listdir(VIDEO_PATH)

        m3u8_obj = m3u8.load(url)
        m3u8_urls = [m3u8_obj.base_uri + ts for ts in m3u8_obj.files]
        # 设置视频路径待处理
        video_name = "{}.mp4".format(tittle)
        video_path = VIDEO_PATH + video_name
        # if video_name in videos:
        #     logging.info(f"视频{video_name}已存在，无需重新下载")
        #     print(f"视频{video_name}已存在，无需重新下载")
        # 开始拼接ts视频
        logging.info(f"开始下载{tittle}...")
        # 调试
        print(f"开始下载{tittle}...")
        time_start = time.time()
        # 进度条展示
        print(f"该视频解析出{len(m3u8_urls)}个ts文件")
        logging.info(f"该视频解析出{len(m3u8_urls)}个ts文件")
        # 设置ts文件顺序
        index = 0
        for ts_url in tqdm(m3u8_urls):
            try:
                ts_data = requests.get(url=ts_url, timeout=120, verify=False)

                logging.info("正在获取第{}个ts文件....".format(index))
                print("正在获取第{}个ts文件....".format(index))
            except TimeoutError as e:
                logging.error("获取第{}个ts数据异常".format(index))
                print("获取第{}个ts数据异常".format(index))
                # ts_data = requests.get(url=url, timeout=120)
                break
            else:
                if ts_data.status_code == 200:
                    with open(video_path, "ab+") as fp:
                        fp.write(ts_data.content)
                else:
                    logging.info(f"下载{tittle}的ts数据时状态请求异常....")
                    print(f"下载{tittle}时状态请求异常....")
            index += 1
        logging.info("耗时%.2f秒，%s下载完成！！！" % (time.time() - time_start, tittle))
        print("耗时%.2f秒，%s下载完成！！！" % (time.time() - time_start, tittle))

    # 方法优化
    @Timer.timer
    def get_ts_datas(self, m3u8_base_url=None, ts_path=None):
        # 防止视频下架，做重试超时处理
        try:
            m3u8_obj = wait_until(func=m3u8.load, timeout=3, msg=f"获取{m3u8_base_url}资源超时", m3u8_base_url=m3u8_base_url)
            print("获取m3u8地址成功！！！")
        except TimeoutError:
            print("已重试，获取m3u8资源失败！！")
            m3u8_obj = m3u8.load(m3u8_base_url)
        m3u8_urls = [m3u8_obj.base_uri + ts for ts in m3u8_obj.files]
        m3u8_files = [ts for ts in m3u8_obj.files]
        # 开始拼接ts视频
        logging.info(f"开始下载{m3u8_base_url}...")
        # 调试
        print(f"开始下载{m3u8_base_url}...")
        # 进度条展示
        print(f"该视频解析出{len(m3u8_urls)}个ts文件")
        logging.info(f"该视频解析出{len(m3u8_urls)}个ts文件")

        # 获取视频片段ts数据（异步协程）
        # 定义会话超时
        timeout = aiohttp.ClientTimeout(total=600)

        async def _get_ts_data(url):
            name = url.split("/")[-1]
            try:
                logging.info("正在获取{}....".format(name))
                print("正在获取{}....".format(name))
                async with ClientSession(timeout=timeout) as session:
                    async with session.get(url=url, timeout=timeout) as response:
                        status_code = response.status
                        response = await response.read()
            except ConnectionError or requests.exceptions.ProxyError or asyncio.exceptions.TimeoutError as e:
                logging.error("获取{}数据异常：{}".format(name, e.strerror))
                print("获取{}数据异常:{}".format(name, e.strerror))
            else:
                if status_code == 200:
                    with open(ts_path + "/" + name, "wb+") as fp:
                        fp.write(response)
                else:
                    logging.info(f"下载{name}数据时状态请求异常....")
                    print(f"下载{name}时状态请求异常....")

        # 设置ts文件顺序
        if ts_path is None:
            ts_path = './ts_data/'
        exist_ts = os.listdir(ts_path)
        retry_ts = set(exist_ts) ^ set(m3u8_files)
        print(f"本次需要下载{len(retry_ts)}个ts文件，开始批量下载....")
        logging.info(f"本次需要下载{len(retry_ts)}个ts文件，开始批量下载....")
        m3u8_urls = [m3u8_obj.base_uri + ts for ts in retry_ts]
        while True:
            exist_ts = os.listdir(ts_path)
            retry_ts = set(exist_ts) ^ set(m3u8_files)
            if len(retry_ts) < 1:
                return False
            try:
                async def main(url_list, ts_path):
                    return await asyncio.gather(
                        *[_get_ts_data(url) for url in tqdm(url_list, desc="Downloading: ") if
                          url.split("/")[-1] not in os.listdir(ts_path)])

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main(m3u8_urls, ts_path))

            except ConnectionError or OSError or TimeoutError as e:
                print(f"获取ts文件发生异常：{e.strerror}")
                logging.info(f"获取ts文件发生异常：{e.strerror}")
                exist_ts = os.listdir(ts_path)
                retry_ts = set(exist_ts) ^ set(m3u8_files)
                if len(retry_ts) >= 1:
                    m3u8_urls = [m3u8_obj.base_uri + ts for ts in retry_ts]
                    print(f"本次需要下载{len(m3u8_urls)}个ts文件，开始批量下载....")
                    logging.info(f"本次需要下载{len(m3u8_urls)}个ts文件，开始批量下载....")
                else:
                    return False

    # 优化（待调试）
    @Timer.timer
    def ts_datas_to_video(self, video_path=None, tittle=None):
        # ts文件存放路径
        path = './ts_data/'
        if video_path is None:
            video_path = './retry_video/'
        if tittle is None:
            tittle = '测试sf'
        files = os.listdir(path)
        # 遍历ts文件，删除空文件
        for file in files:
            tittle = file
            ts_path = path + file
            ts_files = os.listdir(ts_path)
            if len(ts_files) > 0:
                files = sorted(ts_files, key=lambda x: int(x.split(".")[0]))
                from tqdm import tqdm
                for ts_file in tqdm(files, desc="正在视频格式转换："):
                    ts_data_path = ts_path + "/" + ts_file
                    if os.path.exists(ts_data_path):
                        with open(ts_data_path, "rb") as f1:
                            with open("{}{}.mp4".format(video_path, tittle), 'ab+') as f2:
                                f2.write(f1.read())
                    else:
                        print(f"该{ts_file}不存在.....")
                #
                #     #todo 后置步骤，删除ts文件(暂不执行)
                #     # os.system("rm -rf {}*".format(ts_path))

            else:
                # 排除编码错误影响，例如命名为（691(673558.m3u8)）
                name = ts_path.split("(")[0]
                # 删除空文件夹
                os.system("rm -rf {}*".format(name))
                print(f"{tittle}已经被删除")


# 调试
# FindNewWorld().find_picture(url="https://www.pexels.com/zh-cn/search/people%20smiling/", num=10)
# FindNewWorld().find_dy_video()
FindNewWorld().find_study_videos(flag=1)
# FindNewWorld().ts_datas_to_video(tittle="大文件")
# FindNewWorld().get_ts_datas(m3u8_base_url="https://la.killcovid2021.com/m3u8/672577/672577.m3u8", time_out=240)
# FindNewWorld().get_ts_datas(m3u8_base_url="https://la.killcovid2021.com/m3u8/669419/669419.m3u8",ts_path=" ./ts_data/452(673214.m3u8)")

# url = "https://la.killcovid2021.com/m3u8/669419/669419.m3u8"
# FindNewWorld().get_ts_datas(m3u8_base_url=url, time_out=60)

# if __name__ == '__main__':
#     pass

# https://la2.killcovid2021.com/m3u8/673214/673214.m3u8
# ./ts_data/452(673214.m3u8)
