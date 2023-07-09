import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("Login/credentials.json")

firebase_admin.initialize_app(cred, {'databaseURL' : "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})


#Creating data into the realtime database

# data = {
#     "First Name": "Jun Ming",
#     "Last Name": "Ng", 
#     "Birthdate": "20/07/2005",
#     "Email": "mrngjunming@gmail.com"
# }
# data = {
#     "First Name": "Jay Krish",
#     "Last Name": "Vijendra", 
#     "Birthdate": "20/07/2005",
#     "Email": "nightsinker.2005@gmail.com"
# }

# data = {
#     "First Name": "Pin Shien",
#     "Last Name": "Seah", 
#     "Birthdate": "14/07/2005",
#     "Email": "seahpinshien@gmail.com"
# }

# ref = db.reference("Users/customer/account_details")
# ref.push(data)

def get_data():
    ref = db.reference("Users/staff/account_details")
    data = ref.get()
    return data

print(get_data())