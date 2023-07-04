# import pyrebase
import firebase_admin
from firebase_admin import db

config = {
    "apiKey": "AIzaSyBTdJ-q5cuHwkH7iZ9Np2fyFJEeCujN0Jg",
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
    "messagingSenderId": "521940680838",
    "appId": "1:521940680838:web:96e15f16f11bb306c91107",
    "measurementId": "G-QMBGXFXJET"
}

firebase = firebase_admin.initialize_app(config)
database = firebase.database()

data = {"First Name": "Jun Ming", "Last Name": "Ng" , "Birthdate": "20/07/2005" , "Email": "mrngjunming@gmail.com"}
database.child("users").child("staff").child("account_details").set(data)

