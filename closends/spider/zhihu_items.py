"""
@author: Jiale Xu
@date: 2017/11/04
@desc: Items of zhihu scraping.
"""

import re
from closends.spider.base_item import SocialMediaItem
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# 知乎条目基类
class ZhihuItem(SocialMediaItem):
    pass


# 知乎用户信息条目类
class ZhihuUserItem(ZhihuItem):
    def __init__(self):
        self.id = id  # ID
        self.name = ''  # 用户名
        self.gender = 0  # 性别 0为女 1为男 -1为未知
        self.avatar_url = ''  # 头像链接
        self.business = ''  # 行业
        self.headline = ''  # 一句话描述
        self.description = ''  # 个人介绍
        self.question_count = 0  # 提问数
        self.answer_count = 0  # 回答数
        self.article_count = 0  # 文章数
        self.voteup_count = 0  # 得到的赞同数
        self.thanked_count = 0  # 得到的感谢数
        self.favorited_count = 0  # 得到的收藏数
        self.following_count = 0  # 关注数
        self.follower_count = 0  # 粉丝数
        self.following_topic_count = 0  # 关注的话题数
        self.following_column_count = 0  # 关注的专栏数
        self.following_question_count = 0  # 关注的问题数
        self.following_favlist_count = 0  # 关注的收藏夹数
        self.educations = []  # 教育经历
        self.employments = []  # 职业经历
        self.locations = []  # 居住地

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        if self.gender == 0:
            string += 'Gender: 男' + '\n'
        elif self.gender == 1:
            string += 'Gender: 女' + '\n'
        else:
            string += 'Gender: 未知' + '\n'
        string += 'Avatar Url: ' + str(self.avatar_url) + '\n'
        string += 'Business: ' + str(self.business) + '\n'
        string += 'Headline: ' + str(self.headline) + '\n'
        string += 'Description: ' + str(self.description) + '\n'
        string += 'Question Count: ' + str(self.question_count) + '\n'
        string += 'Answer Count: ' + str(self.answer_count) + '\n'
        string += 'Article Count: ' + str(self.article_count) + '\n'
        string += 'Vote-up Count: ' + str(self.voteup_count) + '\n'
        string += 'Thanked Count: ' + str(self.thanked_count) + '\n'
        string += 'Favorited Count: ' + str(self.favorited_count) + '\n'
        string += 'Following Count: ' + str(self.following_count) + '\n'
        string += 'Follower Count: ' + str(self.follower_count) + '\n'
        string += 'Following Topic Count: ' + str(self.following_topic_count) + '\n'
        string += 'Following Column Count: ' + str(self.following_column_count) + '\n'
        string += 'Following Question Count: ' + str(self.following_question_count) + '\n'
        string += 'Following Favlist Count: ' + str(self.following_favlist_count) + '\n'
        string += 'Educations: ' + '; '.join([str(edu) for edu in self.educations]) + '\n'
        string += 'Employments: ' + '; '.join([str(emp) for emp in self.employments]) + '\n'
        string += 'Locations: ' + '; '.join([str(loc) for loc in self.locations]) + '\n'
        return string

    def __hash__(self):
        return hash(self.name)


# 知乎用户教育经历条目类
class ZhihuEducationItem(ZhihuItem):
    def __init__(self):
        self.school = ''  # 学校
        self.major = ''  # 专业

    def __str__(self):
        string = 'School: ' + str(self.school) + ', Major:' + str(self.major)
        return string

    def __hash__(self):
        return hash(self.__str__())


# 知乎用户职业经历条目类
class ZhihuEmploymentItem(ZhihuItem):
    def __init__(self):
        self.company = ''  # 公司名
        self.job = ''  # 职位名

    def __str__(self):
        string = 'Company: ' + str(self.company) + ', Job: ' + str(self.job)
        return string

    def __hash__(self):
        return hash(self.__str__())


# 知乎问题条目类
class ZhihuQuestionItem(ZhihuItem):
    def __init__(self):
        self.id = 0  # 问题ID
        self.title = ''  # 标题
        self.create_time = ''  # 创建时间
        self.update_time = ''  # 更新时间
        self.content = ''  # 内容
        self.follower_count = 0  # 关注数
        self.visit_count = 0  # 浏览数
        self.comment_count = 0  # 评论数
        self.topics = []  # 话题标签列表

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Title: ' + str(self.title) + '\n'
        string += 'Create Time: ' + str(self.create_time) + '\n'
        string += 'Update Time: ' + str(self.update_time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Follower Count: ' + str(self.follower_count) + '\n'
        string += 'Visit Count: ' + str(self.visit_count) + '\n'
        string += 'Comment Count: ' + str(self.comment_count) + '\n'
        string += 'Topics: ' + '; '.join([str(top) for top in self.topics]) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# 知乎答案条目类
class ZhihuAnswerItem(ZhihuItem):
    def __init__(self):
        self.id = 0  # 答案ID
        self.author = ''  # 答主
        self.question_id = 0  # 问题ID
        self.create_time = ''  # 创建时间
        self.update_time = ''  # 更新时间
        self.content = ''  # 内容
        self.voteup_count = ''  # 赞同数
        self.comment_count = ''  # 评论数

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Author: ' + str(self.author) + '\n'
        string += 'Question ID: ' + str(self.question_id) + '\n'
        string += 'Create Time: ' + str(self.create_time) + '\n'
        string += 'Update Time: ' + str(self.update_time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Vote-up Count: ' + str(self.voteup_count) + '\n'
        string += 'Comment Count: ' + str(self.comment_count) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# 知乎用户动态条目
class ZhihuActivityItem(ZhihuItem):
    def __init__(self):
        self.id = 0                     # 动态ID（时间戳）
        self.verb = ''                  # 动态类型
        self.create_time = ''           # 时间
        self.actor = ''                 # 主人
        self.target_user_name = ''      # 目标用户名
        self.target_user_avatar = ''    # 目标头像链接
        self.target_user_headline = ''  # 目标用户简介
        self.target_user_url = ''       # 目标用户主页链接
        self.target_title = ''          # 目标标题内容
        self.target_title_url = ''      # 目标标题链接
        self.target_content = ''        # 目标内容
        self.target_content_url = ''    # 目标内容链接
        self.action_text = ''           # 动态类型文字
        self.thumbnail = ''             # 缩略图

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Verb: ' + str(self.verb) + '\n'
        string += 'Create Time: ' + str(self.create_time) + '\n'
        string += 'Actor: ' + str(self.actor) + '\n'
        string += 'Target User Name: ' + str(self.target_user_name) + '\n'
        string += 'Target User Avatar: ' + str(self.target_user_avatar) + '\n'
        string += 'Target User Headline: ' + str(self.target_user_headline) + '\n'
        string += 'Target User Url: ' + str(self.target_user_url) + '\n'
        string += 'Target Title: ' + str(self.target_title) + '\n'
        string += 'Target Title Url: ' + str(self.target_title_url) + '\n'
        string += 'Target Content: ' + str(self.target_content) + '\n'
        string += 'Target Content Url: ' + str(self.target_content_url) + '\n'
        string += 'Action Text: ' + str(self.action_text) + '\n'
        string += 'Thumbnail: ' + str(self.thumbnail) + '\n'
        return string

    def convert_format(self):
        time_str = re.split('\s+', self.create_time)
        time_str[1] = str(months.index(time_str[1]))
        pub_date = time_str[-1] + '-' + time_str[1] + '-' + time_str[2] + ' ' + time_str[-2]

        zhihu = {}
        zhihu['pub_date'] = pub_date
        zhihu['action_type'] = str(self.action_text)

        zhihu['target_user_name'] = str(self.target_user_name)
        zhihu['target_user_head'] = str(self.target_user_avatar)
        zhihu['target_user_url'] = str(self.target_user_url)
        zhihu['target_user_headline'] = str(self.target_user_headline)

        zhihu['target_title'] = str(self.target_title)
        zhihu['target_title_url'] = str(self.target_title_url)
        zhihu['target_content'] = str(self.target_content)
        zhihu['target_content_url'] = str(self.target_content_url)
        zhihu['cover_image'] = str(self.thumbnail)
        return zhihu

    def __hash__(self):
        return hash(self.id)
