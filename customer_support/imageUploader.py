import pyrebase
from dotenv import load_dotenv
import urllib

class FirebaseStorageClient():
    def __init__(self, config, bucket):
        self.firebase = pyrebase.initialize_app(config)
        self.bucket = bucket

    def upload(self, file_path, filename):
        storage_ref = self.firebase.storage().child(f"{self.bucket}/{filename}")
        storage_ref.put(file_path)
        return "success"

    def get_url(self, filename):
        encoded_filename = urllib.parse.quote(filename)
        url = f"https://firebasestorage.googleapis.com/v0/b/kaki-db097.appspot.com/o/{self.bucket}%2F{encoded_filename}?alt=media"
        return url



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