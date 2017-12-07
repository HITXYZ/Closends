"""
@author : Jiale Xu
@date: 2017/11/11
@desc: Search zhihu users and get html.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.request import quote
from closends.spider.base_exceptions import MethodParamError
from closends.spider.base_configs import zhihu_search_url, zhihu_header


def get_user_by_search(user, number=1, start=0):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    if not isinstance(number, int):
        raise MethodParamError('Parameter \'number\' must be an instance of \'int\'!')
    if number <= 0:
        number = 1
    position = start
    response = requests.get(zhihu_search_url.format(key=quote(user), offset=position), headers=zhihu_header)
    result = response.json()
    user_tokens = []
    user_htmls = []
    while len(user_tokens) < number:
        for html in result.get('htmls'):
            bs = BeautifulSoup(html, 'lxml')
            user_tokens.append(bs.li.attrs['data-token'])
            user_htmls.append(bs.li)
        if len(result.get('htmls')) < 10:
            break
        if len(user_tokens) < number:
            position += 10
            response = requests.get(zhihu_search_url.format(key=quote(user), offset=position), headers=zhihu_header)
            result = response.json()
    if len(user_tokens) > number:
        user_tokens = user_tokens[:number]
        user_htmls = user_htmls[:number]
    user_infos = []
    for user_li in user_htmls:
        item = []
        item.append(str(user_li.find('img')))
        item.append(str(user_li.find('a', {'class', 'author-link'})))
        item.append(str(user_li.find('span', {'class', 'bio'})))
        item += [str(it) for it in user_li.find_all('a')[-3:]]
        user_infos.append(item)
    return user_tokens, user_infos


def get_user_by_homepage(url):
    if not isinstance(url, str):
        raise MethodParamError('Parameter \'url\' must be an instance of \'str\'!')
    if not re.match(r'https://www\.zhihu\.com/people/.*', url):     # 不合法的主页地址
        return None, None
    user = re.search(r'https://www\.zhihu\.com/people/(.*)', url).group(1).split('/')[0]
    response = requests.get('https://www.zhihu.com/people/' + user + '/activities', headers=zhihu_header)
    if response.status_code == 404:     # 用户不存在
        return None, None
    bs = BeautifulSoup(response.text, 'lxml')
    user_name = bs.find('span', {'class': 'ProfileHeader-name'}).get_text()
    start = 0
    while True:
        user_tokens, user_htmls = get_user_by_search(user=user_name, number=10, start=start)
        if len(user_tokens) == 0:
            break
        for user_token, user_html in zip(user_tokens, user_htmls):
            if user_token == user:
                return user_token, user_html
        start += 10
    return None, None


if __name__ == '__main__':
    print(get_user_by_search('江枫', number=2))
    # print(get_user_by_homepage('https://www.zhihu.com/people/excited-vczh/activities'))
    # print(get_user_by_homepage('https://www.zhihu.com/people/jiang-feng-72-58'))
