import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Report_generation.Admin_classes import *

cred = credentials.Certificate("../Account_management/credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})


if __name__ == "__main__":
    # Create event instances and set attributes
    event1 = events_report()
    event1.__event_name__ = "Event 1"
    event1.__event_date__ = "2023-08-10"
    event1.__venue__ = "Community Center"
    event1.__event_description__ = "A fun community event"
    event1.__time__ = "14:00"
    event1.__overall_in_charge__ = "John Doe"
    event1.__dateposted__ = "2023-08-01"
    event1.__community__="bishan_toa_payoh"

    event2 = events_report()
    event2.__event_name__ = "Event 2"
    event2.__event_date__ = "2023-08-15"
    event2.__venue__ = "Park"
    event2.__event_description__ = "Outdoor picnic"
    event2.__time__ = "12:00"
    event2.__overall_in_charge__ = "Jane Smith"
    event2.__dateposted__ = "2023-08-05"
    event2.__community__ ="bishan_toa_payoh"

    # Save events to Firebase
    event1.save_to_firebase()
    event2.save_to_firebase()

