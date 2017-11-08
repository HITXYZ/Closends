import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def qq_login(qq="445561044", password="@ZG.diligence.CN"):
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # driver = webdriver.Chrome(executable_path="D:/Running_Software/chromedriver.exe") # 可视化界面
    driver = webdriver.PhantomJS(executable_path="D:/Running_Software/phantomjs.exe", service_log_path=os.path.devnull)
    driver.get("https://qzone.qq.com")

    driver.implicitly_wait(2)
    driver.switch_to.frame("login_frame")
    driver.find_element_by_id("switcher_plogin").click()
    driver.find_element_by_id("u").clear()
    driver.find_element_by_id("u").send_keys(qq)
    driver.find_element_by_id("p").clear()
    driver.find_element_by_id("p").send_keys(password)
    driver.find_element_by_id("login_button").click()

    time.sleep(5)
    driver.implicitly_wait(5)

    print(driver.current_url)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return driver.current_url == 'https://user.qzone.qq.com/' + qq
    # return driver.current_url == 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone'


def weibo_login(username="15708328370", password="970526"):
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # driver = webdriver.Chrome(executable_path="D:/Running_Software/chromedriver.exe") # 可视化界面
    driver = webdriver.PhantomJS(executable_path="D:/Running_Software/phantomjs.exe", service_log_path=os.path.devnull)
    driver.get("https://passport.weibo.cn/signin/login")

    wait = WebDriverWait(driver, 5)
    wait.until(ec.visibility_of_element_located((By.ID, "loginName")))
    driver.find_element_by_id("loginName").clear()
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").clear()
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()

    time.sleep(2)
    print(driver.current_url)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return driver.current_url == "https://m.weibo.cn/"


def zhihu_login(username="15708328370", password="!KEXIMEIRUGUO1"):
    print(username, password)
    return True


if __name__ == "__main__":
    print(qq_login())
    print(weibo_login())
    # zhihu_login()
