import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime, timedelta
from calendar import month_abbr
import pyrebase


# config = {
#     "apiKey": "AIzaSyBTdJ-q5cuHwkH7iZ9Np2fyFJEeCujN0Jg",
#     "authDomain": "kaki-db097.firebaseapp.com",
#     "projectId": "kaki-db097",
#     "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "storageBucket": "kaki-db097.appspot.com",
#     "messagingSenderId": "521940680838",
#     "appId": "1:521940680838:web:96e15f16f11bb306c91107",
#     "measurementId": "G-QMBGXFXJET"
# }
#
# firebase = pyrebase.initialize_app(config)
# pyredb = firebase.database()
# pyreauth = firebase.auth()
# pyrestorage = firebase.storage()

def initialize_firebase():
    # Replace 'path/to/your/serviceAccountKey.json' with the path to your Firebase Admin SDK credentials
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id.firebaseio.com'
    })


def extract_record_by_value(key, value_field, target_value, details_fields):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Query Firestore for the specific record
    records_ref = db.collection(key).where(value_field, '==', target_value).limit(1)
    records = records_ref.get()

    for record in records:
        record_data = record.to_dict()
        return record_data

    return None


def extract_last_12_months_values(collection_name, individual_id, value_field):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Get the current date and time
    current_date = datetime.now()

    # Create a dictionary to store the month-value mapping
    month_values = {}

    # Retrieve the values for the last 12 months
    for i in range(12):
        # Calculate the start and end dates for the month
        start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*30)
        end_date = current_date.replace(day=1, hour=23, minute=59, second=59, microsecond=999) - timedelta(days=i*30)
        month_name = month_abbr[start_date.month]

        # Query Firestore for the values within the month for the individual
        records_ref = db.collection(collection_name).where('individual_id', '==', individual_id).where('timestamp', '>=', start_date).where('timestamp', '<=', end_date)
        records = records_ref.get()

        # Calculate the sum of the values for the month
        month_value = sum(record.get(value_field) for record in records)

        # Map the month to the value in the dictionary
        month_values[month_name] = month_value

    return month_values


def extract_top_record_by_value(collection_name, value_field, name_field):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the top record from Firestore
    records_ref = db.collection(collection_name).order_by(value_field, direction='DESCENDING').limit(1)
    records = records_ref.get()

    for record in records:
        record_data = record.to_dict()
        return record_data.get(name_field)

    return None


def extract_top_records(collection_name, value_field, details_fields, limit=5):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the top records from Firestore
    records_ref = db.collection(collection_name).order_by(value_field, direction='DESCENDING').limit(limit)
    records = records_ref.get()

    top_records = []
    for record in records:
        record_data = {}
        # Extract value field
        record_data[value_field] = record.get(value_field)
        # Extract details fields
        for field in details_fields:
            record_data[field] = record.get(field)

        top_records.append(record_data)

    return top_records

def retrieve_participation_count(event_id):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the event document from Firestore
    event_ref = db.collection('events').document(event_id)
    event_doc = event_ref.get()

    # Check if the event document exists
    if event_doc.exists:
        # Retrieve the 'participation_count' field value
        participation_count = event_doc.get('participation_count')

        if participation_count is not None:
            return participation_count
        else:
            return 0  # Participation count not set for the event
    else:
        return 0  # Event document not found in Firestore