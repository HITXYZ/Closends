"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Exceptions of weibo scraping
"""


class WeiboError(Exception):
    pass


class LoginError(WeiboError):
    def __init__(self, value="Login failed!"):
        self.info = value

    def __str__(self):
        return repr(self.info)


class ItemAttrError(WeiboError):
    def __init__(self, attr):
        self.info = "Attribute %s is illegal!" % attr

    def __str__(self):
        return repr(self.info)


class ItemEmptyError(WeiboError):
    def __init__(self, value="This item is invalid since its user id hasn't been initialized!"):
        self.info = value

    def __str__(self):
        return repr(self.info)
