"""
    @author: Jiale Xu
    @date: 2017/11/11
    @desc: Search weibo users and get html
"""
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.request import quote
from exceptions import MethodParamError


search_url = 'http://s.weibo.com/user/{user}&Refer=weibo_user'

driver = webdriver.PhantomJS(executable_path='../phantomjs', service_log_path=os.path.devnull)


def search_user(user=None, number=1):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    if not isinstance(number, int):
        raise MethodParamError('Parameter \'number\' must be an instance of \'int\'!')
    if number <= 0:
        number = 1
    wait = WebDriverWait(driver, 3)
    driver.get(search_url.format(user=quote(user)))
    try:
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pl_personlist')))
        user_divs = driver.find_elements_by_class_name('list_person')
    except TimeoutException:    # 未找到结果或网速太慢
        return [], []
    except NoSuchElementException:      # 未找到结果
        return [], []
    if len(user_divs) >= number:    # 截取前number个搜索结果
        user_divs = user_divs[:number]
    user_ids = []
    user_htmls = []
    for user_div in user_divs:
        user_id = user_div.find_element_by_class_name('person_name').find_element_by_tag_name('a').get_attribute('uid')
        user_ids.append(int(user_id))
        user_htmls.append(user_div.get_attribute('outerHTML'))
    return user_ids, user_htmls


if __name__ == '__main__':
    ids, htmls = search_user('理想三旬', 3)
    for id in ids:
        print(type(id), id)
    for html in htmls:
        print(html)