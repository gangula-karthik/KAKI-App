import json

class Ticket:
    status = ['open', 'in progress', 'resolved']
    def __init__(self, ticket_id, user_id, staff_id, subject, closed_at):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.staff_id = staff_id
        self.subject = subject
        self.status = self.__class__.status[0]
        self.closed_at = closed_at
        self.subject_sentiment = None
        self.ml_priority = None
        self.comments = []
    
    def updateStatus(self, status):
        status = status.lower()
        if status in self.__class__.status:
            self.status = status

    def addComment(self, comment): 
        self.comments.append(comment)
    
    def removeComment(self, commentIndex):
        if commentIndex >= 0 and commentIndex < len(self.comments):
            del self.comments[commentIndex]
        else:
            raise ValueError("Invalid comment index")

    def readComments(self):
        if self.comments:
            return self.comments
        else: 
            return "No comments yet..."

    def updateComments(self, commentIndex, newComment):
        if commentIndex >= 0 and commentIndex < len(self.comments) and newComment and isinstance(newComment, str):
            self.comments[commentIndex] = newComment
        else:
            raise ValueError("Invalid input")
    
    def __str__(self):
        return json.dumps({
            "Ticket ID": self.ticket_id,
            "User ID": self.user_id,
            "Staff ID": self.staff_id,
            "Subject": self.subject,
            "Status": self.status,
            "Closed At": str(self.closed_at),
            "Subject Sentiment": self.subject_sentiment,
            "ML Priority": self.ml_priority,
            "Comments": self.comments
        }, indent=4)
    


# ticket = Ticket(1, 1, 1, "I need help", "2021-01-01")
# ticket.addComment("Hello")
# ticket.addComment("World")
# print(ticket.readComments())

# ticket.updateComments(1, "World!")
# print(ticket.readComments())

# ticket.removeComment(1)
# print(ticket.readComments())

# ticket.updateStatus("resolved")
# print(ticket.status)

# print(ticket)