import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("customer_support/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('user')
print(ref.get())
