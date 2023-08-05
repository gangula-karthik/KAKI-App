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

    # Get the Firebase user
    firebase_user = auth.get_user(user['localId'])

    # Check if the email is verified
    email_verified = firebase_user.email_verified

    if not email_verified:
        # Update user's custom claims to indicate pending email verification
        auth.set_custom_user_claims(user['localId'], {'emailVerified': False})

        # Send the email verification
        pyreauth.send_email_verification(user['idToken'])

        print("Verification email sent. Waiting for email verification...")

        # Wait until the email is verified
        while True:
            firebase_user = auth.get_user(user['localId'])
            email_verified = firebase_user.email_verified
            if email_verified:
                # Update user's custom claims to indicate email verification completed
                auth.set_custom_user_claims(user['localId'], {'emailVerified': True})
                print("Email verified.")
                break
            else:
                print("Email not verified. Waiting...")
                time.sleep(5)  # Add a 5-second delay before checking again
    else:
        print("Email already verified.")

except Exception as e:
    print(f"Authentication failed: {e}")