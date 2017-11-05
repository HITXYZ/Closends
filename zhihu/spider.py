"""
    @author: Jiale Xu
    @date: 2017/11/01
    @desc: Scraper for zhihu
"""
import datetime
import json
import logging
import requests
from zhihu.items import ZhihuUserItem, ZhihuEducationItem, ZhihuEmploymentItem


user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'

follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}'

followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,' \
             'following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,' \
             'following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,' \
             'favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,' \
             'account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,' \
             'is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,' \
             'thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,' \
             'allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,' \
                'badge[?(type=best_answerer)].topics'

followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,' \
                  'badge[?(type=best_answerer)].topics'

log_file = "../logs/zhihu/qzone-log-%s.log" % (datetime.date.today())
logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


class ZhihuSpider:
    @staticmethod
    def scrape_info(self, user=None):
        if user is None:
            return None
        response = requests.get(user_url.format(user=user, include=user_query))
        if response is None:
            return None
        result = json.loads(response.text)
        item = ZhihuUserItem()
        item.id = result.get('id')
        item.name = result.get('name')
        item.avatar_url = result.get('avatar_url')
        item.business = result.get('business').get('name')
        item.headline = result.get('headline')
        item.description = result.get('description')
        item.question_count = result.get('question_count')
        item.answer_count = result.get('answer_count')
        item.article_count = result.get('articles_count')
        item.following_count = result.get('following_count')
        item.follower_count = result.get('follower_count')
        item.vote_to_count = result.get('vote_to_count')
        item.vote_from_count = result.get('vote_from_count')
        item.thank_to_count= result.get('thank_to_count')
        item.thank_from_count = result.get('thank_from_count')
        for education in result.get('educations'):
            edu_item = ZhihuEducationItem()
            edu_item.school = education.get('school').get('name')
            edu_item.major = education.get('major').get('name')
            item.educations.append(edu_item)
        for employment in result.get('employments'):
            emp_item = ZhihuEmploymentItem()
            emp_item.company = employment.get('company')
            emp_item.job = employment.get('job')
            item.employments.append(emp_item)
        for location in result.get('locations'):
            item.locations.append(location.get('name'))
        return item

    @staticmethod
    def scrape_follows(self, user=None, number = 10):
        if user is None:
            return []
        response = requests.get(follows_url)


if __name__ == '__main__':
    spider = ZhihuSpider()
