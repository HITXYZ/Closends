"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Exceptions of weibo scraping
"""


class ScraperError(Exception):
    pass


class LoginError(ScraperError):
    def __init__(self, value='Login failed!'):
        self.info = value

    def __str__(self):
        return repr(self.info)


class SpiderInitError(ScraperError):
    def __init__(self, value='Spider initialization failed!'):
        self.info = value

    def __str__(self):
        return repr(self.info)


class SpiderItemError(ScraperError):
    def __init__(self, value='Invalid item!'):
        self.info = value
    
    def __str__(self):
        return repr(self.info)
