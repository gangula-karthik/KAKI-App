import pyrebase
from dotenv import load_dotenv

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


class ChatService:
    def __init__(self, firebase_config):
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.db = self.firebase.database()

    def send_message(self, conversation_id, message):
        self.db.child("conversations").child(conversation_id).push(message)

    def get_conversation(self, conversation_id):
        conversation = self.db.child("conversations").child(conversation_id).get().val()
        return conversation