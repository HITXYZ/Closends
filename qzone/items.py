"""
    @author: Jiale Xu
    @date: 1997/10/27
    @desc: Items of qzone scraping
"""
from baseitem import ScrapeItem


class QzoneItem(ScrapeItem):
    pass


class QzoneUserItem(QzoneItem):
    qq = None
    name = None

    def __str__(self):
        return 'QQ: ' + str(self.qq) + '; Name: ' + str(self.name)

    def __hash__(self):
        return hash(self.qq)


class QzoneEmotionItem(QzoneItem):
    id = None
    owner = QzoneUserItem()
    time = None
    content = None
    pictures = []
    source_name = None
    location = None
    visitors = []
    likers = []
    comments = []

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
    repost_source = QzoneUserItem()
    repost_reason = None

    def __init__(self):
        QzoneEmotionItem.__init__(self)

    def __str__(self):
        string = QzoneEmotionItem.__str__(self)
        string += 'Repost Source: ' + str(self.repost_source) + '\n'
        string += 'Repost Reason: ' + str(self.repost_reason) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class QzoneCommentItem(QzoneItem):
    commenter = QzoneUserItem()
    time = None
    content = None
    pictures = []
    replies = []

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
    replier = QzoneUserItem()
    replyto = QzoneUserItem()
    time = None
    content = None

    def __str__(self):
        return str(self.replier.name) + ' reply to ' + str(self.replyto.name) + ': ' + str(self.content)

    def __hash__(self):
        return hash(self.content)


class QzoneMessageItem(QzoneItem):
    id = None
    owner = QzoneUserItem()
    poster = QzoneUserItem()
    time = None
    content = None
    replies = []

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
    replier = QzoneUserItem()
    time = None
    content = None

    def __str__(self):
        return str(self.replier.name) + 'replied: ' + str(self.content)

    def __hash__(self):
        return hash(self.content)
