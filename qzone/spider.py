"""
    @author: Jiale Xu
    @date: 2017/10/26
    @desc: Scraper for qzone
"""
import datetime
import json
import logging
import os
import re
import requests
import time
import traceback

from math import ceil
from selenium import webdriver

from qzone.items import *


emotion_base_url = "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=%s" \
                           "&ftype=0&sort=0&pos=%d&num=20&replynum=100&g_tk=%s&callback=_preloadCallback" \
                   "&code_version=1&format=jsonp&need_private_comment=1"

comment_base_url = "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?uin=%s" \
                   "&tid=%s&ftype=0&sort=0&pos=0&num=%d&g_tk=%s&callback=_preloadCallback&code_version=1" \
                   "&format=jsonp&need_private_comment=1"

like_base_url = "https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?uin=%s&" \
                "unikey=http%%3A%%2F%%2Fuser.qzone.qq.com%%2F%s%%2Fmood%%2F%s.1&begin_uin=0&query_count=100&" \
                "if_first_page=1&g_tk=%s"

visitor_base_url = "https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_single?" \
                   "uin=%s&appid=311&blogid=%s&param=%s&ref=qzfeeds&beginNum=1&needFriend=1&num=500&g_tk=%s"

message_base_url = "https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=%s&hostUin=%s" \
                   "&start=%d&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk=%s"

headers = {"User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
           "Referer": "https://qzs.qq.com/qzone/app/mood_v6/html/index.html"}

log_file = "qzone-log-%s.log" % (datetime.date.today())
logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


# QQ空间计算g_tk的算法
def get_gtk(p_skey):
    hash = 5381
    for i in range(0, len(p_skey)):
        hash += (hash << 5) + ord(p_skey[i])
    return hash & 2147483647


class QzoneSpider:
    def __init__(self, qq=None, password=None, cookie=None):
        if cookie is None:
            if qq is None or password is None:
                from exceptions import SpiderInitError
                raise SpiderInitError()
            self.qq = qq
            self.password = password
            self.driver = webdriver.PhantomJS(executable_path="../phantomjs")
            self.cookie = {}
            self.gtk = None
            self.login(qq=self.qq, password=self.password)
        else:
            if not os.path.exists(cookie):
                from exceptions import SpiderInitError
                raise SpiderInitError()
            self.load_cookie(path=cookie)

    def login(self, qq=None, password=None):
        if qq is None or password is None:
            qq, password = self.qq, self.password
        self.driver.maximize_window()
        self.driver.get("https://qzone.qq.com")
        logging.info("Opening the qzone login page...")
        self.driver.implicitly_wait(5)

        # 模拟登陆
        self.driver.switch_to.frame("login_frame")
        self.driver.find_element_by_id("switcher_plogin").click()
        self.driver.find_element_by_id("u").clear()
        self.driver.find_element_by_id("u").send_keys(qq)
        self.driver.find_element_by_id("p").clear()
        self.driver.find_element_by_id("p").send_keys(password)
        self.driver.find_element_by_id("login_button").click()

        logging.info("Login to qzone...")
        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.cookie = {}
        cookies = self.driver.get_cookies()
        for item in cookies:
            self.cookie[item["name"]] = item["value"]
        logging.info("Get cookie successfully.")

        p_skey = self.cookie["p_skey"]
        self.gtk = get_gtk(p_skey)      # 使用p_skey计算g_tk
        logging.info("Get g_tk successfully.")

    def scrape_emotion(self, qq=None):
        if self.cookie is None or self.gtk is None:
            logging.warning("Invalid cookie or g_tk.")
            return []
        if qq is None:
            qq = self.qq
        logging.info("Scraping emotions of %s." % qq)
        emotion_pre_url = emotion_base_url % (qq, 0, self.gtk)
        response_text = requests.get(emotion_pre_url, cookies=self.cookie).text
        response = json.loads(response_text[17:-2])

        if response["code"] < 0:           # 没有空间访问权限
            logging.warning("No access to the qzone of %s." % qq)
            return []
        total = response["total"]               # 获取说说总数
        if total == 0:
            logging.info("No emotion in the qzone of %s." % qq)
            return []
        page_number = int(ceil(total * 1.0 / 20))    # 获取页数

        emotion_list = []
        pos = 0
        for i in range(page_number):
            emotion_url = emotion_base_url % (qq, pos, self.gtk)
            logging.info("Scraping emotion page %d: %s." % (i, emotion_url))
            emotion_text = requests.get(emotion_url, cookies=self.cookie, headers=headers).text
            emotion_response = json.loads(emotion_text[17:-2])
            pos += 20       # 每发出一次请求获取接下来20条说说
            if emotion_response["msglist"] is None:     # 所有说说已读取完毕
                break

            for emotion in emotion_response["msglist"]:
                logging.info("Scraping emotion: %s." % emotion["tid"])
                if "rt_tid" in emotion.keys():     # 转发说说
                    item = RepostEmotionItem()
                    item.content = emotion["rt_con"]["content"]
                    item.repost_source.qq = emotion["rt_uin"]
                    item.repost_source.name = emotion["rt_uinname"]
                    item.repost_reason = emotion["content"]
                else:       # 原创说说
                    item = EmotionItem()
                    item.content = emotion["content"]

                item.id = emotion["tid"]
                item.owner.qq = emotion["uin"]
                item.owner.name = emotion["name"]
                item.time = emotion["createTime"]

                if "pic" in emotion.keys():         # 带图说说
                    for pic in emotion["pic"]:
                        pic_url = pic["pic_id"].replace("\/", "/")
                        item.pictures.append(pic_url)
                if "source_name" in emotion.keys():
                    item.source_name = emotion["source_name"]       # 设备信息
                if emotion["lbs"]["idname"] != "":      # 有位置信息
                    item.location = emotion["lbs"]["idname"]
                elif "story_info" in emotion.keys():    # 照片含有位置信息
                    item.location = emotion["story_info"]["lbs"]["idname"]

                visitor_url = visitor_base_url % (qq, item.id, item.id, self.gtk)
                visitor_text = requests.get(visitor_url, cookies=self.cookie, headers=headers).text
                if visitor_text[10:-2][-1] == '}':
                    visitor_response = json.loads(visitor_text[10:-2])
                else:
                    visitor_response = json.loads(visitor_text[10:-3])
                if visitor_response["code"] == 0 and visitor_response["data"]["totalNum"] > 0:  # 有权访问说说访客且有人访问说说
                    for visitor in visitor_response["data"]["list"]:
                        visitor_item = QzoneUserItem()
                        visitor_item.qq = visitor["uin"]
                        visitor_item.name = visitor["name"]
                        item.visitors.append(visitor_item)

                like_url = like_base_url % (self.qq, qq, item.id, self.gtk)
                like_content = requests.get(like_url, cookies=self.cookie, headers=headers).content  # 请求获取点赞列表
                like_response = json.loads(like_content.decode("utf-8")[10:-3])
                if like_response["code"] == 0 and like_response["data"]["total_number"] > 0:   # 请求成功且有人点赞
                    for like in like_response["data"]["like_uin_info"]:
                        liker_item = QzoneUserItem()
                        liker_item.qq = like["fuin"]
                        liker_item.name = like["nick"]
                        item.likers.append(liker_item)

                if emotion["cmtnum"] > 0:       # 有评论
                    if emotion["commentlist"] is None or emotion["cmtnum"] > len(emotion["commentlist"]):     # 评论未加载完毕
                        comment_url = comment_base_url % (qq, emotion["tid"], emotion["cmtnum"], self.gtk)
                        comments_text = requests.get(comment_url, cookies=self.cookie, headers=headers).text
                        comments_response = json.loads(comments_text[17:-2])
                        comments = comments_response["commentlist"]
                    else:       # 评论已加载完毕
                        comments = emotion["commentlist"]
                    if comments is None:    # 评论无法加载
                        emotion_list.append(item)
                        continue
                    for comment in comments:
                        comment_item = CommentItem()
                        comment_item.commenter.qq = comment["uin"]
                        comment_item.commenter.name = comment["name"]
                        comment_item.time = comment["createTime2"]
                        comment_item.content = comment["content"]
                        if "list_3" in comment.keys():      # 评论有回复
                            for reply in comment["list_3"]:
                                reply_item = CommentReplyItem()
                                reply_item.replier.qq = reply["uin"]
                                reply_item.replier.name = reply["name"]
                                reply_content = reply["content"]
                                if re.match(r"@\{.+\}.*", reply_content):
                                    reply_item.replyto.qq = re.search(r"uin:(.*?),", reply_content).group(1)
                                    reply_item.replyto.name = re.search(r"nick:(.*?),", reply_content).group(1)
                                    reply_item.content = re.search(r"auto:1\}(.*)", reply_content).group(1)
                                else:
                                    reply_item.content = reply_content
                                reply_item.time = reply["createTime2"]
                                comment_item.replies.append(reply_item)
                        if "pic" in comment.keys():         # 评论带图
                            for pic in comment["pic"]:
                                pic_url = pic["b_url"].replace("\/", "/")       # 处理图片链接
                                comment_item.pictures.append(pic_url)
                        item.comments.append(comment_item)
                emotion_list.append(item)
                logging.info("Succeed in scraping emotion: %s." % emotion["tid"])
        return emotion_list

    def scrape_message(self, qq=None):
        if self.cookie is None or self.gtk is None:
            logging.warning("Invalid cookie or g_tk.")
            return []
        if qq is None:
            qq = self.qq
        logging.info("Scraping messages of %s." % qq)
        message_pre_url = message_base_url % (self.qq, qq, 0, self.gtk)
        response_text = requests.get(message_pre_url, cookies=self.cookie).text
        response = json.loads(response_text[10:-2])

        if response["code"] < 0:       # 没有空间访问权限
            logging.warning("No access to the qzone of %s." % qq)
            return []
        total = response["data"]["total"]      # 获取留言总数
        if total == 0:
            logging.info("No message in the qzone of %s." % qq)
            return []
        page_number = int(ceil(total * 1.0 / 10))   # 获取页数

        message_list = []
        pos = 0
        for i in range(page_number):
            message_url = message_base_url % (self.qq, qq, pos, self.gtk)
            logging.info("Scraping message page %d: %s." % (i, message_url))
            message_text = requests.get(message_url, cookies=self.cookie, headers=headers).text
            message_response = json.loads(message_text[10:-2])
            pos += 10
            if message_response["data"]["commentList"] is None:     # 所有留言已抓取完毕
                break

            for message in message_response["data"]["commentList"]:
                logging.info("Scraping message: %s" % message["id"])
                item = MessageItem()
                item.id = message["id"]
                item.owner.qq = qq
                item.time = message["pubtime"]
                if message["secret"] == 0:      # 公开留言
                    item.poster.qq = message["uin"]
                    item.poster.name = message["nickname"]
                    item.content = message["ubbContent"]
                    for reply in message["replyList"]:
                        reply_item = MessageReplyItem()
                        reply_item.replier.qq = reply["uin"]
                        reply_item.replier.name = reply["nick"]
                        reply_item.time = reply["time"]
                        reply_item.content = reply["content"]
                        item.replies.append(reply_item)
                else:
                    item.content = "黄钻私密留言"
                message_list.append(item)
                logging.info("Succeed in scraping message: %s." % message["id"])
        return message_list

    def save_cookie(self, path="./cookie.txt"):
        if self.cookie == {} or self.gtk is None:
            return
        file_cookie = open(path, 'w')
        for key in self.cookie:
            file_cookie.write(key + '=' + str(self.cookie[key]) + '\n')
        file_cookie.write("g_tk=" + str(self.gtk) + "\n")
        file_cookie.write("qq=" + str(self.qq))
        file_cookie.close()
        logging.info("Save cookie successfully.")

    def load_cookie(self, path="./cookie.txt"):
        if not os.path.exists(path):
            return
        self.cookie = {}
        file_cookie = open(path, 'r')
        for line in file_cookie:
            lst = line.strip().split('=')
            if lst[0] == "g_tk":
                self.gtk = int(lst[1])
            elif lst[0] == "qq":
                self.qq = lst[1]
            else:
                self.cookie[lst[0]] = lst[1]
        file_cookie.close()
        logging.info("Load cookie successfully.")

    def quit(self):
        logging.info("Stop scrapping.")
        if hasattr(self, "driver"):
            self.driver.quit()


if __name__ == "__main__":
    from exceptions import SpiderInitError
    spider = QzoneSpider(cookie="./cookie.txt")
    try:
        messages = spider.scrape_message("1844338962")
        for message in messages:
            print(message)
    except SpiderInitError:
        traceback.print_exc()
    finally:
        spider.quit()
