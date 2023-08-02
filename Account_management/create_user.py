from flask import Flask, render_template, request , session ,redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase

app = Flask(__name__)
app.secret_key = 'who420is420in12paris'

cred = credentials.Certificate("Account_management/credentials.json")
firebase_admin.initialize_app(cred)

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


# email = input('Enter email: ')
# password = input('Enter password: ')

# username = input('Enter username: ')
user_data = pyredb.child("Users").child("Consumer").child('6W9Z3kRoBRWAEMNskqpjfLnGCUk2').get().val()

print(user_data)

# user = auth.get_user_by_email(email)
# try:
#     user = auth.get_user_by_email(email)
    
#     verified_user = auth.verify_password(email=email, password=password)

#     if user.uid == verified_user.uid:
#         email_verified = user.email_verified
#         print(f"Email verified: {email_verified}")
#     else:
#         print("Invalid email or password.")

# except:
#     print("Authentication failed:")


# user = auth.create_user(
#     email=email,
#     password=password,
# )


# verification_link = auth.generate_email_verification_link(email)

# print("User created successfully:", user.uid)

# print('email veriifcation:', verification_link)
