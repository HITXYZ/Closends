"""
    @author: Jiale Xu
    @date: 2017/10/26
    @desc: Scraper for qzone
"""
import json
import re
import requests
import time
import traceback

from selenium import webdriver

from bs4 import BeautifulSoup


# QQ空间计算g_tk的算法
def get_gtk(p_skey):
    hash = 5381
    for i in range(0, len(p_skey)):
        hash += (hash << 5) + ord(p_skey[i])
    return hash & 2147483647


class QzoneSpider:
    def __init__(self, qq, password):
        self.qq = qq
        self.password = password
        self.driver = webdriver.PhantomJS(executable_path="../phantomjs")
        self.cookie = {}
        self.gtk = None
        self.qzonetoken = None
        self.emotion_url = ""

    def login(self):
        self.driver.maximize_window()
        self.driver.get("https://qzone.qq.com")
        self.driver.implicitly_wait(5)

        # 模拟登陆
        self.driver.switch_to.frame("login_frame")
        self.driver.find_element_by_id("switcher_plogin").click()
        self.driver.find_element_by_id("u").clear()
        self.driver.find_element_by_id("u").send_keys(self.qq)
        self.driver.find_element_by_id("p").clear()
        self.driver.find_element_by_id("p").send_keys(self.password)
        self.driver.find_element_by_id("login_button").click()

        time.sleep(5)
        self.driver.implicitly_wait(5)
        self.cookie = {}
        cookies = self.driver.get_cookies()
        for item in cookies:
            self.cookie[item["name"]] = item["value"]
        p_skey = self.cookie["p_skey"]
        self.gtk = get_gtk(p_skey)      # 使用p_skey计算g_tk

        bs = BeautifulSoup(self.driver.page_source, "lxml")
        scripts = bs.find_all("script")
        for script in scripts:
            code = script.get_text()
            if re.match(r"window\.g_qzonetoken = .*", code):        # 从js代码中找到qzonetoken
                self.qzonetoken = re.search(r"try\{return \"(.+?)\";\}", code).group(1)
                break

        print(self.cookie)
        print(self.gtk)
        print(self.qzonetoken)

    def scrape_emotion(self, qq=None):
        if self.cookie is None or self.gtk is None or self.qzonetoken is None:
            return []
        if qq is None:
            qq = self.qq
        base_url = "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?" \
                      "uin=%s&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk=%s&callback=_preloadCallback&" \
                      "code_version=1&format=jsonp&need_private_comment=1&qzonetoken=%s&g_tk=%d"
        emotion_url = base_url % (qq, self.gtk, self.qzonetoken, self.gtk)
        response_text = requests.get(emotion_url, cookies=self.cookie).text
        print(response_text)
        response = json.loads(response_text[17, -2])

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    spider = QzoneSpider("******", "******")
    try:
        spider.login()
    except:
        traceback.print_exc()
    finally:
        spider.quit()
