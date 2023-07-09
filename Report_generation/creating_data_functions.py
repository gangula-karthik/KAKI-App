import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from io import BytesIO


def add_report_to_firebase(report_id, report_content, collection_name):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Create a new document in the specified collection with the report ID as the document ID
    report_ref = db.collection(collection_name).document(report_id)

    # Set the report content as the data in the document
    report_ref.set(report_content)

    # Close the Firestore client
    db.terminate()


def delete_report_from_firebase(report_id, collection_name):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Delete the report document
    reports_ref = db.collection(collection_name)
    report_ref = reports_ref.document(report_id)
    report_ref.delete()

    # Close the Firestore client
    db.terminate()