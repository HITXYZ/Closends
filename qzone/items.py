"""
    @author: Jiale Xu
    @date: 1997/10/27
    @desc: Items of qzone scraping
"""
from base_item import SocialMediaItem


# QQ空间条目基类
class QzoneItem(SocialMediaItem):
    pass


# QQ空间用户信息条目类
class QzoneUserItem(QzoneItem):
    def __init__(self):
        self.qq = None      # QQ号
        self.name = None    # 昵称

    def __str__(self):
        return 'QQ: ' + str(self.qq) + '; Name: ' + str(self.name)

    def __hash__(self):
        return hash(self.qq)


# QQ空间说说条目类
class QzoneEmotionItem(QzoneItem):
    def __init__(self):
        self.id = None                  # 说说ID
        self.owner = QzoneUserItem()    # 主人
        self.time = None                # 时间
        self.content = None             # 内容
        self.pictures = []              # 图片列表
        self.source_name = None         # 设备名称
        self.location = None            # 位置
        self.visitors = []              # 浏览者列表
        self.likers = []                # 点赞者列表
        self.comments = []              # 评论列表

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Owner: ' + str(self.owner) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Pictures: ' + '; '.join([str(pic) for pic in self.pictures]) + '\n'
        string += 'Source Name: ' + str(self.source_name) + '\n'
        string += 'Location: ' + str(self.location) + '\n'
        string += 'Visitor Number: ' + str(len(self.visitors)) + '\n'
        string += 'Like Number: ' + str(len(self.likers)) + '\n'
        string += 'Comment Number: ' + str(len(self.comments)) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# QQ空间转发说说条目类
class QzoneRepostEmotionItem(QzoneEmotionItem):
    def __init__(self):
        QzoneEmotionItem.__init__(self)
        self.repost_source = QzoneUserItem()    # 转发来源
        self.repost_reason = None               # 转发理由

    def __str__(self):
        string = QzoneEmotionItem.__str__(self)
        string += 'Repost Source: ' + str(self.repost_source) + '\n'
        string += 'Repost Reason: ' + str(self.repost_reason) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# QQ空间说说评论条目类
class QzoneCommentItem(QzoneItem):
    def __init__(self):
        self.commenter = QzoneUserItem()    # 评论者
        self.time = None                    # 评论时间
        self.content = None                 # 评论内容
        self.pictures = []                  # 评论图片列表
        self.replies = []                   # 评论回复列表

    def __str__(self):
        string = ''
        string += 'Commenter: ' + str(self.commenter) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Pictures: ' + '; '.join([str(pic) for pic in self.pictures]) + '\n'
        string += 'Reply Number: ' + str(len(self.replies)) + '\n'
        return string

    def __hash__(self):
        return hash(self.content)


# QQ空间说说评论回复条目类
class QzoneCommentReplyItem(QzoneItem):
    def __init__(self):
        self.replier = QzoneUserItem()      # 回复者
        self.replyto = QzoneUserItem()      # 回复对象
        self.time = None                    # 回复时间
        self.content = None                 # 回复内容

    def __str__(self):
        return str(self.time) + ' ' + str(self.replier.name) + \
               ' reply to ' + str(self.replyto.name) + ': ' + str(self.content)

    def __hash__(self):
        return hash(self.content)


# QQ空间留言条目类
class QzoneMessageItem(QzoneItem):
    def __init__(self):
        self.id = None                      # 留言ID
        self.owner = QzoneUserItem()        # 主人
        self.poster = QzoneUserItem()       # 留言者
        self.time = None                    # 留言时间
        self.content = None                 # 留言内容
        self.replies = []                   # 留言回复列表

    def __str__(self):
        string = ''
        string += 'Owner: ' + str(self.owner) + '\n'
        string += 'Poster: ' + str(self.poster) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Reply Number: ' + str(len(self.replies)) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# QQ空间留言回复条目类
class QzoneMessageReplyItem(QzoneItem):
    def __init__(self):
        self.replier = QzoneUserItem()      # 回复者
        self.time = None                    # 回复时间
        self.content = None                 # 回复内容

    def __str__(self):
        return str(self.time) + ' ' + str(self.replier.name) + 'replied: ' + str(self.content)

    def __hash__(self):
        return hash(self.content)
