import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("Account_management\credentials.json")

firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

email = "gkars.2@gmail.com"
password = "nightsinker2010"


user = auth.create_user(
    email=email,
    password=password
)

print("User created successfully:", user.uid)