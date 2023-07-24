import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Saved_Report:
    report_id_count = 0

    def __init__(self, report_id):
        self.__report_id__ = report_id

    def save_to_firebase(self):
        report_data = {
            "report_id": self.__report_id__,
        }

        # Save the report data to Firebase Realtime Database
        ref = db.reference("/saved_reports")  # Replace "/saved_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("/saved_reports")  # Replace "/saved_reports" with the path where your data is stored
        report_ref = ref.child(report_id).get()

        if report_ref:
            return cls(report_ref.get("report_id"))
        else:
            return None

    def update_to_firebase(self, attribute_name, new_value):
        # Update specific attribute of the report in Firebase Realtime Database
        ref = db.reference("/saved_reports")  # Replace "/saved_reports" with the path where your data is stored
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})


class Indi_Report(Saved_Report):
    def __init__(self):
        Saved_Report.report_id_count += 1
        super().__init__(Saved_Report.report_id_count)
        self.__report_id__ = Saved_Report.report_id_count
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__pieData__ = None
        self.__neighboursHelped__ = None
        self.__activities__ = None
        self.__pieLabel__ = None

    # ... (getter and setter methods as before)

    def save_to_firebase(self):
        report_data = {
            "report_id": self.__report_id__,
            "leaderboard": self.__leaderboard__,
            "current_month": self.__CurrentMonth__,
            "current_year": self.__CurrentYear__,
            "list_months": self.__listMonths__,
            "line_data": self.__lineData__,
            "pie_data": self.__pieData__,
            "neighbours_helped": self.__neighboursHelped__,
            "activities": self.__activities__,
            "pie_label": self.__pieLabel__,
        }

        # Save the report data to Firebase Realtime Database
        ref = db.reference("/reports")  # Replace "/reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    def load_from_firebase(self, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("/reports")  # Replace "/reports" with the path where your data is stored
        report_ref = ref.child(report_id).get()

        if report_ref:
            self.__report_id__ = report_ref.get("report_id")
            self.__leaderboard__ = report_ref.get("leaderboard")
            self.__CurrentMonth__ = report_ref.get("current_month")
            self.__CurrentYear__ = report_ref.get("current_year")
            self.__listMonths__ = report_ref.get("list_months")
            self.__lineData__ = report_ref.get("line_data")
            self.__pieData__ = report_ref.get("pie_data")
            self.__neighboursHelped__ = report_ref.get("neighbours_helped")
            self.__activities__ = report_ref.get("activities")
            self.__pieLabel__ = report_ref.get("pie_label")
            return True
        else:
            return False

    def update_to_firebase(self, attribute_name, new_value):
        # Update specific attribute of the report in Firebase Realtime Database
        ref = db.reference("/reports")  # Replace "/reports" with the path where your data is stored
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})


class Com_Report(Saved_Report):
    def __init__(self):
        Saved_Report.report_id_count += 1
        super().__init__(Saved_Report.report_id_count)
        self.__report_id__ = Saved_Report.report_id_count
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__pieData__ = None
        self.__MostContributed__ = None
        self.__activities__ = None
        self.__pieLabel__ = None

    # ... (getter and setter methods as before)

    def save_to_firebase(self):
        report_data = {
            "report_id": self.__report_id__,
            "leaderboard": self.__leaderboard__,
            "current_month": self.__CurrentMonth__,
            "current_year": self.__CurrentYear__,
            "list_months": self.__listMonths__,
            "line_data": self.__lineData__,
            "pie_data": self.__pieData__,
            "most_contributed": self.__MostContributed__,
            "activities": self.__activities__,
            "pie_label": self.__pieLabel__,
        }

        # Save the report data to Firebase Realtime Database
        ref = db.reference("/com_reports")  # Replace "/com_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("/com_reports")  # Replace "/com_reports" with the path where your data is stored
        report_ref = ref.child(report_id).get()

        if report_ref:
            com_report_instance = cls()
            com_report_instance.__report_id__ = report_ref.get("report_id")
            com_report_instance.__leaderboard__ = report_ref.get("leaderboard")
            com_report_instance.__CurrentMonth__ = report_ref.get("current_month")
            com_report_instance.__CurrentYear__ = report_ref.get("current_year")
            com_report_instance.__listMonths__ = report_ref.get("list_months")
            com_report_instance.__lineData__ = report_ref.get("line_data")
            com_report_instance.__pieData__ = report_ref.get("pie_data")
            com_report_instance.__MostContributed__ = report_ref.get("most_contributed")
            com_report_instance.__activities__ = report_ref.get("activities")
            com_report_instance.__pieLabel__ = report_ref.get("pie_label")
            return com_report_instance
        else:
            return None

    def update_to_firebase(self, attribute_name, new_value):
        # Update specific attribute of the report in Firebase Realtime Database
        ref = db.reference("/com_reports")  # Replace "/com_reports" with the path where your data is stored
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})


class trans_report(Saved_Report):
    def __init__(self):
        Saved_Report.report_id_count += 1
        super().__init__(Saved_Report.report_id_count)
        self.__transactionDataIn__ = None
        self.__transactionDataOut__ = None
        self.__NoTransactionData = None

    # ... (getter and setter methods as before)

    def save_to_firebase(self):
        report_data = {
            "report_id": self._Saved_Report__report_id__,  # Use the protected attribute from the parent class
            "transaction_data_in": self.__transactionDataIn__,
            "transaction_data_out": self.__transactionDataOut__,
            "no_transaction_data": self.__NoTransactionData,
        }

        # Save the report data to Firebase Realtime Database
        ref = db.reference("/trans_reports")  # Replace "/trans_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("/trans_reports")  # Replace "/trans_reports" with the path where your data is stored
        report_ref = ref.child(report_id).get()

        if report_ref:
            trans_report_instance = cls()
            trans_report_instance._Saved_Report__report_id__ = report_ref.get("report_id")
            trans_report_instance.__transactionDataIn__ = report_ref.get("transaction_data_in")
            trans_report_instance.__transactionDataOut__ = report_ref.get("transaction_data_out")
            trans_report_instance.__NoTransactionData = report_ref.get("no_transaction_data")
            return trans_report_instance
        else:
            return None

    def update_to_firebase(self, attribute_name, new_value):
        # Update specific attribute of the report in Firebase Realtime Database
        ref = db.reference("/trans_reports")  # Replace "/trans_reports" with the path where your data is stored
        report_ref = ref.child(self._Saved_Report__report_id__)  # Use the protected attribute from the parent class
        report_ref.update({attribute_name: new_value})


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
        ref = db.reference("/events_reports")  # Replace "/events_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("/events_reports")  # Replace "/events_reports" with the path where your data is stored
        report_ref = ref.child(report_id).get()

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

    def update_to_firebase(self, attribute_name, new_value):
        # Update specific attribute of the report in Firebase Realtime Database
        ref = db.reference("/events_reports")  # Replace "/events_reports" with the path where your data is stored
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})
