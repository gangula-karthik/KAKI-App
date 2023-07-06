import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import fasttext

nltk.download('vader_lexicon')

class Ticket:
    status = ['open', 'in progress', 'resolved']
    topic = ['technical support', 'payment', 'others']
    def __init__(self, ticket_id, user_id, staff_id, subject):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.staff_id = staff_id
        self.subject = subject
        self.status = self.__class__.status[0]
        self.closed_at = None
        self.calculate_subject_sentiment(self.subject)
        self.topic = None
        self.comments = []
        self.opened_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.closed_at = None
        self.addMLPriority(self.subject)
        self.replies = []
    
    def addMLPriority(self, subject):
        model = fasttext.load_model("customer_support/model.bin")
        priority = model.predict(subject)
        self.ml_priority = priority[0][0].replace("__label__", "").replace("\"", "")

    def addTopic(self, topic):
        topic = topic.lower()
        if topic in self.__class__.topic:
            self.topic = topic
        else:
            raise ValueError("Invalid topic")
        
    def updateTopic(self, new_topic):
        new_topic = new_topic.lower()
        if new_topic in self.__class__.topic:
            self.topic = new_topic
        else:
            raise ValueError("Invalid topic")
    
    def deleteTopic(self):
        self.topic = None

    
    def updateStatus(self, status):
        status = status.lower()
        if status in self.__class__.status:
            self.status = status
            if self.status == "resolved": 
                self.closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
        
    def calculate_subject_sentiment(self, subject):
        sia = SentimentIntensityAnalyzer()
        polarity_scores = sia.polarity_scores(subject)

        if polarity_scores['compound'] > 0.05:
            self.subject_sentiment = "positive"
        elif polarity_scores['compound'] < -0.05:
            self.subject_sentiment = "negative"
        else:
            self.subject_sentiment = "neutral"

    def addReply(self, reply):
        self.replies.append(reply)
    
    def __str__(self):
        return json.dumps({
            "Ticket ID": self.ticket_id,
            "User ID": self.user_id,
            "Staff ID": self.staff_id,
            "Subject": self.subject,
            "Topic": self.topic,
            "Status": self.status,
            "Subject Sentiment": self.subject_sentiment,
            "ML Priority": self.ml_priority,
            "Comments": self.comments,
            "Opened At": self.opened_at,
            "Closed At": self.closed_at
        }, indent=4)
    


if __name__ == "__main__":
    ticket = Ticket(1, 1, 1, "I can't find the 'Product_IP' of my phone.")
    ticket.addComment("Hello")
    ticket.addComment("World")
    print(ticket.readComments())

    ticket.updateComments(1, "World!")
    print(ticket.readComments())

    ticket.removeComment(1)
    print(ticket.readComments())

    ticket.updateStatus("resolved")
    print(ticket.status)

    print(ticket)