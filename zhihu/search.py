"""
    @author : Jiale Xu
    @date: 2017/11/11
    @desc: Search zhihu users and get html
"""
import requests
from bs4 import BeautifulSoup
from urllib.request import quote, urlretrieve
from exceptions import MethodParamError


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

search_url = 'https://www.zhihu.com/search?type=people&q={key}'


def search_user(user=None, number=1):
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
    if user_ul is None:     # 未搜索到任何用户
        return [], []
    user_lis = user_ul.find_all('li')
    if len(user_lis) > number:
        user_lis = user_lis[:number]
    for user_li in user_lis:
        user_tokens.append(user_li.attrs['data-token'])
        user_htmls.append(user_li.prettify())
    return user_tokens, user_htmls


if __name__ == '__main__':
    tokens, htmls = search_user('于晟建', 3)
    for user_token in tokens:
        print(user_token)
    for user_html in htmls:
        print(user_html)
