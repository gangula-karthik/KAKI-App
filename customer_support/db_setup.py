import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def database_init():
    cred = credentials.Certificate("customer_support/serviceAccountKey.json")

    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

    print("Database initialized")