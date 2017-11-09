import os
from urllib.request import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def check_weibo_user(username):
    # driver = webdriver.Chrome(executable_path="D:/Running_Software/chromedriver.exe") # 可视化界面
    driver = webdriver.PhantomJS(executable_path="D:/Running_Software/phantomjs.exe", service_log_path=os.path.devnull)
    url = "http://s.weibo.com/user/" + quote(username) + "&Refer=weibo_user"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "pl_personlist")))
    item = driver.find_element_by_class_name("list_person")
    search_html = item.get_attribute('innerHTML')
    driver.close()
    return search_html