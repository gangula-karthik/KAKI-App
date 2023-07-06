import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import flask as flask

cred = credentials.Certificate("Login\credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def create_user(email, password):
    user = auth.create_user(
        email=email,
        password=password
    )
    print("User created successfully:"), user.uid

# email = "jaykrish.vijendra.20@gmail.com"
# password = "nightsinker2010"

# user = auth.create_user(
#     email=email,
#     password=password
# )

# print("User created successfully:", user.uid)