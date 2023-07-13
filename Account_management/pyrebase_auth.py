import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase

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

cred = credentials.Certificate("Account_management/credentials.json")

firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

firebase = pyrebase.initialize_app(config)

db = firebase.database()
pyreauth = firebase.auth()
storage = firebase.storage()

email = input('Enter email: ')
password = input('Enter password: ')


# user = auth.create_user(
#     email=email,
#     password=password,
# )

# print("User created successfully:", user.uid)




try:
    user = pyreauth.sign_in_with_email_and_password(email, password)
    print(user)
except:
    print("Authentication failed:")