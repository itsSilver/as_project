# coding=utf-8


import urllib2
import random
import re


# 获取www.marathonbet.com的对应队伍的比赛的url
def get_current_url(url, ranks): 
    user_agent = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like     Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    ]
    get_user_agent = random.choice(user_agent)
    headers = {"User-Agent":get_user_agent}
    urls = "https://www.marathonbet.com/en/live/popular"
    request = urllib2.Request(urls, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    pattern = re.compile(r'%s","href":"(.+?(\d+))'%ranks)
    re_obj = pattern.search(html)
    url = re.sub(r'/\w+/?$', "", url)
    if re_obj is not None:
        hrefs = re_obj.group(1)
        return url + hrefs
    else:
        return ""
