"""
@author: Jiale Xu
@date: 2017/11/20
@desc: Search tieba users.
"""
import re
import chardet
import requests
from bs4 import BeautifulSoup
from urllib.request import quote
from exceptions import MethodParamError
from configs import tieba_user_profile_url


def get_user_by_search(user):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
    response = requests.get(tieba_user_profile_url.format(user=quote(user)))
    encoding = chardet.detect(response.content).get('encoding')
    bs = BeautifulSoup(response.content.decode(encoding), 'lxml')
    if bs.find('title').get_text() == '贴吧404':  # 用户不存在
        return None, None
    html = bs.find('div', {'id': 'userinfo_wrap'})
    html.find('div', {'class': 'userinfo_right'}).extract()
    return user, html.prettify()


def get_user_by_homepage(url):
    if not isinstance(url, str):
        raise MethodParamError('Parameter \'url\' isn\'t an instance of type \'str\'!')
    if not re.match(r'http://tieba.baidu.com/home/main\?un=.*&.*', url) and not re.match(       # 不合法的主页地址
            r'http://tieba.baidu.com/home/main\?un=.*', url):
        return None, None
    response = requests.get(url)
    encoding = chardet.detect(response.content).get('encoding')
    bs = BeautifulSoup(response.content.decode(encoding), 'lxml')
    if bs.find('title').get_text() == '贴吧404':  # 用户不存在
        return None, None
    html = bs.find('div', {'id': 'userinfo_wrap'})
    html.find('div', {'class': 'userinfo_right'}).extract()
    user = html.find('span', {'class': 'userinfo_username'}).get_text()
    return user, html.prettify()


if __name__ == '__main__':
    user, html = get_user_by_search('愛你沒法說')
    print(user)
    print(html)

    user, html = get_user_by_homepage('http://tieba.baidu.com/home/main?un=%E6%84%9B%E4%BD%A0%E6%B2%92%E6%B3%95%E8%AA%AA')
    print(user)
    print(html)