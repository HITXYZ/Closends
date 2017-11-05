"""
    @author: Jiale Xu
    @date: 2017/11/04
    @desc: Items of zhihu scraping
"""
from items import ScrapeItem


class ZhihuItem(ScrapeItem):
    pass


class ZhihuUserItem(ZhihuItem):
    def __init__(self):
        self.id = id
        self.name = None
        self.avatar_url = None
        self.business = None
        self.headline = None
        self.description = None
        self.question_count = 0
        self.answer_count = 0
        self.article_count = 0
        self.following_count = 0
        self.follower_count = 0
        self.vote_to_count = 0
        self.vote_from_count = 0
        self.thank_to_count = 0
        self.thank_from_count = 0
        self.educations = []
        self.employments = []
        self.locations = []

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Avatar Url: ' + str(self.avatar_url) + '\n'
        string += 'Business: ' + str(self.business) + '\n'
        string += 'Headline: ' + str(self.headline) + '\n'
        string += 'Description: ' + str(self.description) + '\n'
        string += 'Question Count: ' + str(self.question_count) + '\n'
        string += 'Answer Count: ' + str(self.answer_count) + '\n'
        string += 'Article Count: ' + str(self.article_count) + '\n'
        string += 'Following Count: ' + str(self.following_count) + '\n'
        string += 'Follower Count: ' + str(self.follower_count) + '\n'
        string += 'Vote-to Count: ' + str(self.vote_to_count) + '\n'
        string += 'Vote-from Count: ' + str(self.vote_from_count) + '\n'
        string += 'Thank-to Count: ' + str(self.thank_to_count) + '\n'
        string += 'Thank-from Count: ' + str(self.thank_from_count) + '\n'
        return string

    def __hash__(self):
        return hash(self.name)


class ZhihuEducationItem(ZhihuItem):
    def __init__(self):
        self.school = None
        self.major = None

    def __str__(self):
        string = 'School: ' + str(self.school) + '; Major:' + str(self.major)
        return string

    def __hash__(self):
        return hash(self.__str__())


class ZhihuEmploymentItem(ZhihuItem):
    def __init__(self):
        self.company = None
        self.job = None

    def __str__(self):
        string = 'Company: ' + str(self.company) + '; Job: ' + str(self.job)
        return string

    def __hash__(self):
        return hash(self.__str__())