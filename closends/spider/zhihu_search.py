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
from closends.spider.base_configs import zhihu_search_url, zhihu_headers


def get_user_by_search(user=None, number=1):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    if not isinstance(number, int):
        raise MethodParamError('Parameter \'number\' must be an instance of \'int\'!')
    number = 1 if number < 1 else number
    response = requests.get(zhihu_search_url.format(key=quote(user)), headers=zhihu_headers)
    bs = BeautifulSoup(response.text, 'lxml')
    user_tokens = []
    user_htmls = []
    user_ul = bs.find('ul', {'class': 'users'})
    if user_ul is None:  # 未搜索到任何用户
        return [], []
    user_lis = user_ul.find_all('li')
    if len(user_lis) > number:
        user_lis = user_lis[:number]
    for user_li in user_lis:
        user_tokens.append(user_li.attrs['data-token'])
        item = []
        item.append(str(user_li.find('img')))
        item.append(str(user_li.find('a', {'class', 'name-link'})))
        item.append(str(user_li.find('span', {'class', 'bio'})))
        item += [str(it) for it in user_li.find_all('a')[-3:]]
        user_htmls.append(item)
    return user_tokens, user_htmls


def get_user_by_homepage(url):
    if not isinstance(url, str):
        raise MethodParamError('Parameter \'url\' must be an instance of \'str\'!')
    if not re.match(r'https://www\.zhihu\.com/people/.*', url):  # 不合法的主页地址
        return None, None
    user = re.search(r'https://www\.zhihu\.com/people/(.*)', url).group(1).split('/')[0]
    response = requests.get('https://www.zhihu.com/people/' + user + '/activities', headers=zhihu_headers)
    if response.status_code == 404:  # 用户不存在
        return None, None
    user_tokens, user_htmls = get_user_by_search(user=user, number=1)
    if len(user_tokens) > 0 and len(user_htmls) > 0:
        return user_tokens[0], user_htmls[0]
    return None, None


if __name__ == '__main__':
    print(get_user_by_search('江枫', 1))
    # print(get_user_by_homepage('https://www.zhihu.com/people/excited-vczh/activities'))
    # print(get_user_by_homepage('https://www.zhihu.com/people/jiang-feng-72-58'))
