import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import pyrebase
# import fasttext
from dotenv import load_dotenv

nltk.download('vader_lexicon')

config = {
    "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
    "messagingSenderId": "521940680838",
    "appId": "1:521940680838:web:96e15f16f11bb306c91107",
    "measurementId": "G-QMBGXFXJET"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Ticket:
    status = ['open', 'in progress', 'resolved']
    topic = ['billing', 'technical', 'listing', 'other']
    def __init__(self, user_id, subject, descriptions, topic):
        self.user_id = user_id
        self.staff_id = None
        self.subject = subject
        self.status = self.__class__.status[0]
        self.closed_at = None
        self.calculate_subject_sentiment(self.subject)
        if topic in self.__class__.topic:
            self.topic = topic
        else:
            raise ValueError("Invalid topic")
        self.descriptions = descriptions
        self.opened_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.closed_at = None
        # self.addMLPriority(self.subject)
        self.images = []
        self.replies = [] # replies should be a list of dictionaries
        try:
            self.ticket_id = db.child('/tickets').push(self.__dict__)['name']
            db.child(f'/tickets/{self.ticket_id}').update({"ticket_id": self.ticket_id})
            print("Data pushed to Firebase successfully.")
        except Exception as e:
            print(f"Error while pushing data to Firebase: {e}")

    def addStaffID(self, staff_id):
        self.staff_id = staff_id
    
    def addMLPriority(self, subject):
        """
        BROKEN: FIX IMMEDIATELY
        """
        # model = fasttext.load_model("/Users/daaa/Downloads/KAKI-App/customer_support/model.bin")
        # priority = model.predict(f"{self.topic} {self.subject} {self.descriptions}")
        # self.ml_priority = priority[0][0].replace("__label__", "").replace("\"", "")

    def addTopic(self, topic):
        topic = topic.lower()
        if topic in self.__class__.topic:
            self.topic = topic
        else:
            raise ValueError("Invalid topic")
    
    def addImages(self, image_url):
        self.images.append(image_url)
        
    def updateTopic(self, ticket_id, new_topic):
        new_topic = new_topic.lower()
        if new_topic in self.__class__.topic:
            self.topic = new_topic
            self.ticket_id = ticket_id
            db.child(f'/tickets/{self.ticket_id}').update({"topic": self.topic})
        else:
            raise ValueError("Invalid topic")
        
    def updateSubject(self, ticket_id, new_subject):
        self.ticket_id = ticket_id
        self.subject = new_subject
        db.child(f'/tickets/{self.ticket_id}').update({"subject": self.subject})

    def updateDescriptions(self, ticket_id, new_descriptions):
        self.ticket_id = ticket_id
        self.descriptions = new_descriptions
        db.child(f'/tickets/{self.ticket_id}').update({"descriptions": self.descriptions})
        
    def deleteTicket(self):
        db.child(f'/tickets/{self.ticket_id}').remove()
        print("Ticket deleted successfully.")
        self.ticket_id = None
        self.user_id = None
        self.staff_id = None
        self.subject = None
        self.status = None
        self.topic = None
        self.descriptions = None
        self.opened_at = None
        self.closed_at = None

    
    def updateStatus(self, status):
        status = status.lower()
        if status in self.__class__.status:
            self.status = status
            if self.status == "resolved": 
                self.closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
        
    def calculate_subject_sentiment(self, subject):
        sia = SentimentIntensityAnalyzer()
        polarity_scores = sia.polarity_scores(subject)

        if polarity_scores['compound'] > 0.05:
            self.subject_sentiment = "positive"
        elif polarity_scores['compound'] < -0.05:
            self.subject_sentiment = "negative"
        else:
            self.subject_sentiment = "neutral"

    def addReply(self, username, reply):
        reply_data = {
            "username": username,
            "reply": reply,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        self.replies.append(reply_data)
        db.child(f'/tickets/{self.ticket_id}/replies').set(self.replies)


    
    def __str__(self):
        return json.dumps({
            "Ticket ID": self.ticket_id,
            "User ID": self.user_id,
            "Staff ID": self.staff_id,
            "Subject": self.subject,
            "Topic": self.topic,
            "Status": self.status,
            "Subject Sentiment": self.subject_sentiment,
            # "ML Priority": self.ml_priority,
            "descriptions": self.descriptions,
            "Opened At": self.opened_at,
            "Closed At": self.closed_at
        }, indent=4)



if __name__ == "__main__": 
    t2 = Ticket("user1", "subject1", "descriptions1", "billing")
    print(t2)
    time.sleep(4)
    t2.updateSubject(t2.ticket_id, "time to punch wall")
    t2.updateTopic(t2.ticket_id, "technical")
    t2.updateDescriptions(t2.ticket_id, "website stole my damn money")
    print(t2)