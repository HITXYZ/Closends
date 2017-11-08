"""
    @author: Jiale Xu
    @date: 1997/10/27
    @desc: Items of qzone scraping
"""
from base_item import SocialMediaItem


class QzoneItem(SocialMediaItem):
    pass


class QzoneUserItem(QzoneItem):
    def __init__(self):
        self.qq = None
        self.name = None

    def __str__(self):
        return 'QQ: ' + str(self.qq) + '; Name: ' + str(self.name)

    def __hash__(self):
        return hash(self.qq)


class QzoneEmotionItem(QzoneItem):
    def __init__(self):
        self.id = None
        self.owner = QzoneUserItem()
        self.time = None
        self.content = None
        self.pictures = []
        self.source_name = None
        self.location = None
        self.visitors = []
        self.likers = []
        self.comments = []

    def __str__(self):
        string = ''
        string += 'Owner: ' + str(self.owner) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Pictures: ' + str(self.pictures) + '\n'
        string += 'Source Name: ' + str(self.source_name) + '\n'
        string += 'Location: ' + str(self.location) + '\n'
        string += 'Visitor Number: ' + str(len(self.visitors)) + '\n'
        string += 'Like Number: ' + str(len(self.likers)) + '\n'
        string += 'Comment Number: ' + str(len(self.comments)) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class QzoneRepostEmotionItem(QzoneEmotionItem):
    def __init__(self):
        QzoneEmotionItem.__init__(self)
        self.repost_source = QzoneUserItem()
        self.repost_reason = None

    def __str__(self):
        string = QzoneEmotionItem.__str__(self)
        string += 'Repost Source: ' + str(self.repost_source) + '\n'
        string += 'Repost Reason: ' + str(self.repost_reason) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class QzoneCommentItem(QzoneItem):
    def __init__(self):
        self.commenter = QzoneUserItem()
        self.time = None
        self.content = None
        self.pictures = []
        self.replies = []

    def __str__(self):
        string = ''
        string += 'Commenter: ' + str(self.commenter) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Pictures: ' + str(self.pictures) + '\n'
        string += 'Reply Number: ' + str(len(self.replies)) + '\n'
        return string

    def __hash__(self):
        return hash(self.content)


class QzoneCommentReplyItem(QzoneItem):
    def __init__(self):
        self.replier = QzoneUserItem()
        self.replyto = QzoneUserItem()
        self.time = None
        self.content = None

    def __str__(self):
        return str(self.replier.name) + ' reply to ' + str(self.replyto.name) + ': ' + str(self.content)

    def __hash__(self):
        return hash(self.content)


class QzoneMessageItem(QzoneItem):
    def __init__(self):
        self.id = None
        self.owner = QzoneUserItem()
        self.poster = QzoneUserItem()
        self.time = None
        self.content = None
        self.replies = []

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


class QzoneMessageReplyItem(QzoneItem):
    def __init__(self):
        self.replier = QzoneUserItem()
        self.time = None
        self.content = None

    def __str__(self):
        return str(self.replier.name) + 'replied: ' + str(self.content)

    def __hash__(self):
        return hash(self.content)
