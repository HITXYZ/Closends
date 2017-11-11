"""
    @author: Jiale Xu
    @date: 2017/11/11
    @desc: Search weibo users and get html
"""
import os
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.request import quote, urlretrieve
from exceptions import MethodParamError


search_url = 'http://s.weibo.com/user/{user}&Refer=weibo_user'

driver = webdriver.PhantomJS(executable_path='../phantomjs', service_log_path=os.path.devnull)


def search_user(user=None, number=1):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    wait = WebDriverWait(driver, 3)
    driver.get(search_url.format(user=quote(user)))
    try:
        captcha_image_parent = driver.find_element_by_class_name('code_img')  # 需要验证码
        captcha_image = captcha_image_parent.find_element_by_tag_name('img')
        captcha_input_parent = driver.find_element_by_class_name('code_input')
        captcha_input = captcha_input_parent.find_element_by_tag_name('input')
        captcha_button = driver.find_element_by_class_name('code_btn')
        urlretrieve(captcha_image.get_attribute('src'), 'captcha.png')
        image = Image.open('captcha.png')
        image.show()
        code = input('Please input the captcha to continue:')
        captcha_input.clear()
        captcha_input.send_keys(code)
        captcha_button.click()
    except NoSuchElementException:  # 无需验证码
        pass
    except OSError:  # 无法识别图片
        return []
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pl_personlist')))
    items = driver.find_elements_by_class_name('list_person')
    if len(items) >= number:  # 截取前number个搜索结果
        items = items[:number]
    return [item.get_attribute('innerHTML') for item in items]


if __name__ == '__main__':
    for i in range(20):
        users = search_user('许家乐', 3)
        print(users)