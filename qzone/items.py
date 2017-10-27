"""
    @author: Jiale Xu
    @date: 1997/10/27
    @desc: Items of qzone scraping
"""


class QzoneUserItem:
    def __init__(self):
        self.qq = None
        self.name = None

    def __str__(self):
        return "QQ: " + str(self.qq) + "; Name: " + str(self.name) + "\n"

    def __hash__(self):
        return hash(self.qq)


class EmotionItem:
    def __init__(self):
        self.id = None
        self.owner = QzoneUserItem()
        self.time = None
        self.content = None
        self.pictures = []
        self.source_name = None
        self.location = None
        self.visit_times = 0
        self.likers = []
        self.comments = []

    def __str__(self):
        string = ""
        string += "Owner: " + str(self.owner) + "\n"
        string += "Time: " + str(self.time) + "\n"
        string += "Content: " + str(self.content) + "\n"
        string += "Source Name: " + str(self.source_name) + "\n"
        string += "Location: " + str(self.location) + "\n"
        string += "Visit Times: " + str(self.visit_times) + "\n"
        string += "Like Number: " + str(len(self.likers)) + "\n"
        string += "Comment Number: " + str(len(self.comments)) + "\n"
        return string

    def __hash__(self):
        return hash(self.id)


class RepostEmotionItem(EmotionItem):
    def __init__(self):
        EmotionItem.__init__(self)
        self.repost_source = QzoneUserItem()
        self.repost_reason = None

    def __str__(self):
        string = EmotionItem.__str__(self)
        string += "Repost Source: " + str(self.repost_source)
        string += "Repost Reason: " + str(self.repost_reason)
        return string

    def __hash__(self):
        return hash(str(self.content) + str(self.repost_reason))


class CommentItem:
    def __init__(self):
        self.time = None
        self.content = None
        self.replies = []
        self.pictures = []

    def __str__(self):
        string = ""
        string += "Time: " + str(self.time) + "\n"
        string += "Content: " + str(self.content) + "\n"
        string += "Reply Number: " + str(len(self.replies)) + "\n"
        return string

    def __hash__(self):
        return hash(self.content)