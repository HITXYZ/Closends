"""
    @author: Jiale Xu
    @date: 2017/11/04
    @desc: Items of zhihu scraping
"""
from baseitem import ScrapeItem


class ZhihuItem(ScrapeItem):
    pass


class ZhihuUserItem(ZhihuItem):
    id = id                        # 用户ID
    name = None                    # 用户名
    gender = 0                     # 性别 0为女 1为男
    avatar_url = None              # 头像链接
    business = None                # 所在领域
    headline = None                # 简介
    description = None             # 个人介绍
    question_count = 0             # 提问数
    answer_count = 0               # 回答数
    article_count = 0              # 文章数
    voteup_count = 0               # 得到的赞同数
    thanked_count = 0              # 得到的感谢数
    favorited_count = 0            # 得到的收藏数
    following_count = 0            # 关注数
    follower_count = 0             # 粉丝数
    following_topic_count = 0      # 关注的话题数
    following_column_count = 0     # 关注的专栏数
    following_question_count = 0   # 关注的问题数
    following_favlist_count = 0    # 关注的收藏夹数
    educations = []                # 教育经历
    employments = []               # 工作经历
    locations = []                 # 所在地

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        if self.gender == 0:
            string += 'Gender: female' + '\n'
        else:
            string += 'Gender: male' + '\n'
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
        string += 'Following Topic Count:' + str(self.following_topic_count) + '\n'
        string += 'Following Column Count: ' + str(self.following_column_count) + '\n'
        string += 'Following Question Count: ' + str(self.following_question_count) + '\n'
        string += 'Following Favlist Count: ' + str(self.following_favlist_count) + '\n'
        return string

    def __hash__(self):
        return hash(self.name)


class ZhihuEducationItem(ZhihuItem):
    school = None
    major = None

    def __str__(self):
        string = 'School: ' + str(self.school) + '; Major:' + str(self.major)
        return string

    def __hash__(self):
        return hash(self.__str__())


class ZhihuEmploymentItem(ZhihuItem):
    company = None
    job = None

    def __str__(self):
        string = 'Company: ' + str(self.company) + '; Job: ' + str(self.job)
        return string

    def __hash__(self):
        return hash(self.__str__())
