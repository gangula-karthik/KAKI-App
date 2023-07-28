import firebase_admin
from firebase_admin import credentials
from firebase_admin import db




config = {
    "apiKey": "AIzaSyBTdJ-q5cuHwkH7iZ9Np2fyFJEeCujN0Jg",
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
    "messagingSenderId": "521940680838",
    "appId": "1:521940680838:web:96e15f16f11bb306c91107",
    "measurementId": "G-QMBGXFXJET"
}

firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()


def extract_data_from_firebase(database_url, service_account_key_path, database_path):
    
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    })

    
    ref = db.reference(database_path)

    
    data = ref.get()

    

    
    firebase_admin.delete_app(firebase_admin.get_app())

    return data