import pyrebase
from dotenv import load_dotenv
import urllib

import urllib.parse
import pyrebase

class FirebaseStorageClient():
    firebase = None

    @classmethod
    def initialize(cls, config):
        if cls.firebase is None:
            cls.firebase = pyrebase.initialize_app(config)

    def __init__(self, bucket):
        if FirebaseStorageClient.firebase is None:
            raise ValueError("Firebase has not been initialized. Call FirebaseStorageClient.initialize(config) first.")
        self.bucket = bucket

    def upload(self, file_path, filename):
        storage_ref = self.firebase.storage().child(f"{self.bucket}/{filename}")
        storage_ref.put(file_path)
        return self.get_url(filename)

    def get_url(self, filename):
        encoded_filename = urllib.parse.quote(filename)
        url = f"https://firebasestorage.googleapis.com/v0/b/kaki-db097.appspot.com/o/{self.bucket}%2F{encoded_filename}?alt=media"
        return url
    
    def delete(self, filename):
        storage_ref = self.firebase.storage().child(f"{self.bucket}/{filename}")
        storage_ref.delete()




if __name__ == "__main__":
    config = {
        "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
        "authDomain": "kaki-db097.firebaseapp.com",
        "projectId": "kaki-db097",
        "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "storageBucket": "kaki-db097.appspot.com",
    }
    firebase_storage_client = FirebaseStorageClient(config, "kaki_social_media")
    url = firebase_storage_client.upload("customer_support/test.png", "onlineEvent.png")
    url = firebase_storage_client.get_url("onlineEvent.png")
    print(url)