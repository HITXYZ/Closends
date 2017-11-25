"""
@author: Jiale Xu
@date: 2017/10/23
@desc: Exceptions of scraping.
"""


class SocialMediaException(Exception):
    pass


class LoginError(SocialMediaException):
    def __init__(self, value='Login failed!'):
        self.info = value

    def __str__(self):
        return repr(self.info)


class SpiderInitError(SocialMediaException):
    def __init__(self, value='Spider initialization failed!'):
        self.info = value

    def __str__(self):
        return repr(self.info)


class MethodParamError(SocialMediaException):
    def __init__(self, value='Invalid item!'):
        self.info = value
    
    def __str__(self):
        return repr(self.info)
