import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# cred = credentials.Certificate('../Account_management/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

class events_report():
    def __init__(self):
        self.__event_name__ = None
        self.__event_date__ = None
        self.__venue__ = None
        self.__event_description__ = None
        self.__time__ = None
        self.__overall_in_charge__ = None
        self.__dateposted__ = None

    # ... (getter and setter methods as before)
    # Getter methods
    def get_event_name(self):
        return self.__event_name__

    def get_event_date(self):
        return self.__event_date__

    def get_venue(self):
        return self.__venue__

    def get_event_description(self):
        return self.__event_description__

    def get_time(self):
        return self.__time__

    def get_overall_in_charge(self):
        return self.__overall_in_charge__

    def get_dateposted(self):
        return self.__dateposted__

    # Setter methods
    def set_event_name(self, event_name):
        self.__event_name__ = event_name

    def set_event_date(self, event_date):
        self.__event_date__ = event_date

    def set_venue(self, venue):
        self.__venue__ = venue

    def set_event_description(self, event_description):
        self.__event_description__ = event_description

    def set_time(self, time):
        self.__time__ = time

    def set_overall_in_charge(self, overall_in_charge):
        self.__overall_in_charge__ = overall_in_charge

    def set_dateposted(self, dateposted):
        self.__dateposted__ = dateposted

    def save_to_firebase(self):
        report_data = {
            "event_name": self.__event_name__,
            "event_date": self.__event_date__,
            "venue": self.__venue__,
            "event_description": self.__event_description__,
            "time": self.__time__,
            "overall_in_charge": self.__overall_in_charge__,
            "date_posted": self.__dateposted__,
        }

        # Save the report data to Firebase Realtime Database
        ref = db.reference("Events")  # Replace "/events_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, UID):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("Events")  # Replace "/events_reports" with the path where your data is stored
        report_ref = ref.child(UID).get()

        if report_ref:
            events_report_instance = cls()
            events_report_instance.__event_name__ = report_ref.get("event_name")
            events_report_instance.__event_date__ = report_ref.get("event_date")
            events_report_instance.__venue__ = report_ref.get("venue")
            events_report_instance.__event_description__ = report_ref.get("event_description")
            events_report_instance.__time__ = report_ref.get("time")
            events_report_instance.__overall_in_charge__ = report_ref.get("overall_in_charge")
            events_report_instance.__dateposted__ = report_ref.get("date_posted")
            return events_report_instance
        else:
            return None

    def update(self, attribute_values):
        # Update specific attributes of the report instance
        for attribute, value in attribute_values.items():
            setattr(self, attribute, value)

        # Save the updated report data to Firebase Realtime Database
        ref = db.reference("Events")
        report_ref = ref.child(self.__event_name__)
        report_data = {
            "event_name": self.__event_name__,
            "event_date": self.__event_date__,
            "venue": self.__venue__,
            "event_description": self.__event_description__,
            "time": self.__time__,
            "overall_in_charge": self.__overall_in_charge__,
            "date_posted": self.__dateposted__,
        }
        report_ref.update(report_data)

