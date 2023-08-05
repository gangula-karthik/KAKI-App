import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase
import time

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

try:
    user = pyreauth.sign_in_with_email_and_password(email, password)
    print(user)

    # Send the email verification
    user_id = user['idToken']
    pyreauth.send_email_verification(user_id)

    # Wait until the email is verified
    while True:
        user = pyreauth.get_account_info(user['idToken'])
        email_verified = user['users'][0]['emailVerified']
        if email_verified:
            print("Email verified.")
            break
        else:
            print("Email not verified. Waiting...")
            time.sleep(5)  # Add a 5-second delay before checking again

except Exception as e:
    print(f"Authentication failed: {e}")