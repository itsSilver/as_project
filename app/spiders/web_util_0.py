# !/usr/bin/python
# coding=utf-8


import urllib
import urllib2
import io, gzip
import random
import json
import os


user_agent = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like     Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    ]
get_user_agent = random.choice(user_agent)


# 从betburger获取数据
def get_betburger_web_content(url):

    # 创建请求头信息
    headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'api-lv.betburger.com',
            'Origin': 'https://www.betburger.com',
            'Referer': 'https://www.betburger.com/arbs/live',
            'User-Agent' : get_user_agent
        }
    
    # 处理所有post请求参数
    formdata = {
            'auto_update': 'true',
            'notification_sound': 'false',
            'notification_popup': 'false',
            'show_event_arbs': 'true',
            'grouped': 'true',
            'per_page': '50',
            'sort_by': 'percent',
            'event_id': '',
            '''
            'event_arb_types[]': '1',
            'event_arb_types[]': '2',
            'event_arb_types[]': '3',
            'event_arb_types[]': '4',
            'event_arb_types[]': '5',
            'event_arb_types[]': '6',
            'event_arb_types[]': '7',
            '''
            'is_live': 'true',
            'search_filter[]': '25555',
        }
    formdata = urllib.urlencode(formdata)
    
    request = urllib2.Request(url, data = formdata, headers = headers)
    return data_formate(request)


# 获取运动的名称
def get_directories(url, url_mid_name):
    work_dir = os.getcwd()
    dir_list = os.listdir(work_dir + '/tmp')
    file_dir = './tmp/' + url_mid_name + '.txt'
    is_open = True
    for dir in dir_list: 
        if dir.split('.')[0] == url_mid_name:
            is_open = False
    headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'api-lv.betburger.com',
            'If-None-Match': "3a0362770e0052df257ccb65039d9110",
            'Origin': 'https://www.betburger.com',
            'Referer': 'https://www.betburger.com/arbs/live',
            'User-Agent': get_user_agent
        }
    if is_open:
        request = urllib2.Request(url, headers = headers) 
        data = data_formate(request)

        if data != "":
            data = json.loads(data)
            with open(file_dir, 'w') as f:
                f.write(str(data))
            return data 
        else:
            return ""
    else:
        with open(file_dir, 'r') as f:
            fstr = f.read()
        return eval(fstr)


# 获取bet_values值
def get_bet_value(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'api-lv.betburger.com',
        'Origin': 'https://www.betburger.com',
        'Referer': 'https://www.betburger.com/arbs/live',
        'User-Agent': get_user_agent
    }
    request = urllib2.Request(url, headers = headers)
    data = data_formate(request)
    
    if data != "":
        data = json.loads(data)
        return data
    else:
        return ""

# 数据格式转化
def data_formate(request):
    try:
        response = urllib2.urlopen(request)
        if response.code == 200:
            if response.info().get('Content-Encoding') == 'gzip':
                buf = io.BytesIO(response.read())
                gf = gzip.GzipFile(fileobj=buf)
                data = gf.read()
                return data
            else:
                return response.read()
    except urllib2.HTTPError as err:
        return err
    except urllib2.URLError as err:
        return err
    else: 
        return ""


if __name__ == '__main__':
    url = 'http://api-lv.betburger.com/api/v1/arbs/pro_search?access_token='
    get_betburger_web_content(url)
