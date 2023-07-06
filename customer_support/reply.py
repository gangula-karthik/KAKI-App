import time

class Reply:
    def __init__(self, replyID, userID, ticketID, Content):
        self.replyID = replyID
        self.userID = userID
        self.ticketID = ticketID
        self.content = Content
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.updated_at = None
        self.deleted_at = None

    def editReply(self, newContent):
        self.content = newContent
        self.updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def deleteReply(self):
        self.content = None
        self.deleted_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def readReply(self):
        if self.content:
            return self.content
        else:
            return "This reply does not exist..."