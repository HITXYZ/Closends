# -*- coding: utf-8 -*-
"""
    @author: Jiale Xu
    @date: 2017/10/12
    @desc: Imitate weibo-login by phantom
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def login(url, account, password):
    def is_login(page):
        match = page.find('"isLogin":true')
        if match:
            return True
        return False

    driver = webdriver.Chrome('D:/Program Files/chromedriver')
    driver.maximize_window()
    driver.get(url)

    # wait for the appearance of needed page elements
    wait = WebDriverWait(driver, 5)
    wait.until(ec.visibility_of_element_located((By.ID, "loginName")))

    # locate page elements
    act_field = driver.find_element_by_id('loginName')
    pwd_field = driver.find_element_by_id("loginPassword")
    submit = driver.find_element_by_id("loginAction")

    # clear the contents inside text fields
    act_field.clear()
    pwd_field.clear()

    # login
    act_field.send_keys(account)
    pwd_field.send_keys(password)
    submit.click()

    time.sleep(2)
    source = driver.page_source.encode('ascii', 'ignore')
    if is_login(source):
        print('登录成功')

    weibo_cookies = driver.get_cookies()
    driver.quit()
    return weibo_cookies


if __name__ == '__main__':
    url_input = 'https://passport.weibo.cn/signin/login'
    act_input = 'your account'
    pwd_input = 'your password'
    cookies = login(url_input, act_input, pwd_input)
