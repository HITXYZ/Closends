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
from closends.spider.base_exceptions import MethodParamError
from closends.spider.base_configs import tieba_user_profile_url


def get_user_by_search(user):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
    response = requests.get(tieba_user_profile_url.format(user=quote(user)))
    encoding = chardet.detect(response.content).get('encoding')
    bs = BeautifulSoup(response.content.decode(encoding), 'lxml')
    if bs.find('title').get_text() == '贴吧404':  # 用户不存在
        return None, None
    html = bs.find('div', {'id': 'userinfo_wrap'})
    head = str(html.find('img').attrs['src'])
    link = str(html.find('div', {'class', 'userinfo_shortcut'}).find('a').attrs['href'])
    sex = html.find('span', {'class', 'userinfo_sex'}).attrs['class'][1][13:]
    age = html.find_all('span')[-4].get_text()
    num = html.find_all('span')[-6].get_text()
    return user, [head, link, sex, age, num]


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
    user = html.find('span', {'class': 'userinfo_username'}).get_text()
    user_data = str(html.find('div', {'class', 'userinfo_userdata'}))
    head = str(html.find('img').attrs['src'])
    link = str(html.find('div', {'class', 'userinfo_shortcut'}).find('a').attrs['href'])
    sex = html.find('span', {'class', 'userinfo_sex'}).attrs['class'][1][13:]
    age = html.find_all('span')[-4].get_text()
    num = html.find_all('span')[-6].get_text()
    return user, [head, link, sex, age, num]


if __name__ == '__main__':
    user, html = get_user_by_search('孤独凤凰战士')
    print(user, html)

    user, html = get_user_by_homepage('https://www.baidu.com/p/%B9%C2%B6%C0%B7%EF%BB%CB%D5%BD%CA%BF?from=tieba')
    print(user, html)
