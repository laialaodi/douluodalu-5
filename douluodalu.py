# -*- coding: utf-8 -*-
# 作者：laialaodi https://github.com/laialaodi
# 本文件遵守 CC-BY-NC-SA 4.0 协议，任何人可以自由复制、散布、展示及演出本作品，但必须署名；且不可作商业用途；
# 仅在遵守与本著作相同的授权条款下，您才能散布由本作品产生的衍生作品

import re
import time

import requests

# 请求头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'}


class DouLuoDaLu5:
    def debug(self) -> None:
        """爬取日志中出错的url"""

        # 读取日志
        with open('error.log', 'r') as f1:
            _content_list = f1.readlines()

        # 再次开始爬取出错的URL
        with open('error.log', 'w') as f1:
            for _content in _content_list:
                _debug_url: str = _content.split(' ')[-1]
                _debug_return_value = self.get_info(_debug_url)
                print(_debug_return_value, end='  ')
                if _debug_return_value != 0:
                    f1.write(
                        f'{time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))} {str(_debug_return_value)} {_debug_url}')
                    print('返回值异常，已记录在日志', end='  ')
                print(_debug_url, end='')
                time.sleep(1)  # 停顿

    @staticmethod
    def get_urls(left: int = 9) -> list:
        """这个函数可以通过主页获取所有章节的网址并返回

        参数
            left: 从第几章开始，由于某些缘故，第一章需要传入9，第二章则传入10，以此类推

        返回值
            一个列表，表示抓取到的网址

            如果list[0] == -1 则代表主页状态码不为200

            list[0] == -2 代表获取过程出错
        """
        _res = requests.get('https://www.soshuw.com/DouLuoDaLuvZhongShengTangSan/', headers=headers)
        if _res.status_code == 200:
            try:
                _new_list = []
                _url_list = re.findall('<dd><a href="(.*?)">.*?</a></dd>', _res.text, flags=re.S)[left:]

                # 获取URL并加入列表
                for _url in _url_list:
                    _new_list.append('https://www.soshuw.com{}'.format(_url))
                return _new_list
            except:
                return [-2]
        else:
            return [-1]

    @staticmethod
    def get_info(url: str) -> int:
        """这个函数可以爬取《斗罗大陆5》全文小说并提取信息

        参数
            url: 要爬取网站的url

        返回值
            0 正常访问、写入

            -1 HTTP状态码不为200

            -2 访问过程出错
        """
        _res = requests.get(url, headers=headers)
        if _res.status_code == 200:
            try:
                _title = str(re.findall(pattern='<h1>(第\d+章 .*?)</h1>', string=_res.text)[0])
                _i = int(url.split('/')[-1].split('.')[0])
                _contents = re.findall(pattern=f'<div class="content" id="con{str(_i)}">(.*?)</div>', string=_res.text,
                                       flags=re.S)  # flag=re.S是跨行匹配
                with open(f'《斗罗大陆5重生唐三》全文小说/{_title}.txt', 'w+') as f:
                    print(_title, end='  ')
                    f.write(_title + '\n')
                    for _content in _contents:
                        _content_copy = _content
                        _content_copy = _content_copy.replace('<br>', '')
                        _content_copy = _content_copy.replace('<br />', '')
                        _content_copy = _content_copy.replace('&nbsp;', ' ')
                        _content_copy = re.sub(pattern='<p>(.*?)</p>', repl='', string=_content_copy, flags=re.S)
                        # 同上，re.S是跨行匹配
                        _content_copy = _content_copy.strip()
                        f.write(_content_copy + '\n')
                return 0
            except:
                return -2
        else:
            return -1

    def run(self, left: int) -> None:
        """这个函数作为主函数

        参数
            link DouLuoDaLu的实例

            mode 模式，可选有
                debug 将出错的URL再爬一遍

                run 正儿八经地运行

            left 从哪一章开始爬取
        """
        urls = self.get_urls(left=left + 9)
        for url in urls:
            return_value = self.get_info(url)
            if return_value != 0:
                print(return_value, end='  ')
                with open('error.log', 'a+') as f:
                    f.write(
                        f'{time.strftime("[%Y-%m-%d %H:%M:%S ERROR]", time.localtime(time.time()))} {str(return_value)} {url}\n')
                print('返回值异常，已记录在日志', end='  ')
            print(url)
            time.sleep(1)
