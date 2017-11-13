"""
    @author : Jiale Xu
    @date: 2017/11/11
    @desc: Search zhihu users and get html
"""
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import quote, urlretrieve
from closends.spider.exceptions import MethodParamError

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

search_url = 'https://www.zhihu.com/search?type=people&q={key}'


def get_user_by_search(user=None, number=1):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    if not isinstance(number, int):
        raise MethodParamError('Parameter \'number\' must be an instance of \'int\'!')
    if number <= 0:
        number = 1
    response = requests.get(search_url.format(key=quote(user)), headers=headers)
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
        user_htmls.append(user_li.prettify())
    return user_tokens, user_htmls


def get_user_by_homepage(url):
    if not isinstance(url, str):
        raise MethodParamError('Parameter \'url\' must be an instance of \'str\'!')
    if not re.match(r'https://www\.zhihu\.com/people/.*', url):  # 不合法的主页地址
        return None, None
    user = re.search(r'https://www\.zhihu\.com/people/(.*)', url).group(1).split('/')[0]
    response = requests.get('https://www.zhihu.com/people/' + user + '/activities', headers=headers)
    if response.status_code == 404:  # 用户不存在
        return None, None
    user_tokens, user_htmls = get_user_by_search(user=user, number=1)
    if len(user_tokens) > 0 and len(user_htmls) > 0:
        return user_tokens[0], user_htmls[0]
    return None, None


if __name__ == '__main__':
    # print(get_user_by_homepage('https://www.zhihu.com/people/excited-vczh/activities')[1])
    print(get_user_by_search("于晟建")[1])
