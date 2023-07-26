import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
        ref = db.reference("Users/Saved_report/events_reports")  # Replace "/events_reports" with the path where you want to store the data
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    @classmethod
    def load_from_firebase(cls, report_id):
        # Load report data from Firebase Realtime Database using the report_id
        ref = db.reference("Users/Saved_report/events_reports")  # Replace "/events_reports" with the path where your data is stored
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
        ref = db.reference("Users/Saved_report/events_reports")  # Replace "/events_reports" with the path where your data is stored
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})

class Com_Report:
    counter = 0

    def __init__(self):
        number = str(Com_Report.counter + 1)
        report_id = 'CR' + number
        self.__report_id__ = report_id
        self.__community_name__ = None
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__pieData__ = None
        self.__MostContributed__ = None
        self.__activities__ = None
        self.__pieLabel__ = None

    # Getter and setter methods for Com_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def set_report_id(self, report_id):
        self.__report_id__ = report_id

    def get_community_name(self):
        return self.__community_name__

    def set_community_name(self, community_name):
        self.__community_name__ = community_name

    def get_leaderboard(self):
        return self.__leaderboard__

    def set_leaderboard(self, leaderboard):
        self.__leaderboard__ = leaderboard

    def get_current_month(self):
        return self.__CurrentMonth__

    def set_current_month(self, current_month):
        self.__CurrentMonth__ = current_month

    def get_current_year(self):
        return self.__CurrentYear__

    def set_current_year(self, current_year):
        self.__CurrentYear__ = current_year

    def get_list_months(self):
        return self.__listMonths__

    def set_list_months(self, list_months):
        self.__listMonths__ = list_months

    def get_line_data(self):
        return self.__lineData__

    def set_line_data(self, line_data):
        self.__lineData__ = line_data

    def get_pie_data(self):
        return self.__pieData__

    def set_pie_data(self, pie_data):
        self.__pieData__ = pie_data

    def get_most_contributed(self):
        return self.__MostContributed__

    def set_most_contributed(self, most_contributed):
        self.__MostContributed__ = most_contributed

    def get_activities(self):
        return self.__activities__

    def set_activities(self, activities):
        self.__activities__ = activities

    def get_pie_label(self):
        return self.__pieLabel__

    def set_pie_label(self, pie_label):
        self.__pieLabel__ = pie_label

    # Add getter and setter methods for other attributes as needed

    # Method to save Com_Report to Firebase
    def save_to_firebase(self):
        report_data = {
            "report_id": self.__report_id__,
            "community_name": self.__community_name__,
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

        ref = db.reference("Admin/All_Com_report/")
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Com_Report from Firebase using report_id
    @classmethod
    def load_from_firebase(cls, target_report_id):
        ref = db.reference("Admin/All_Com_report/")
        report_data = ref.get()
        return report_data


    def delete_from_firebase(self):
        if self.__report_id__:
            ref = db.reference("Admin/All_Com_report/")
            report_ref = ref.child(self.__report_id__)
            report_ref.delete()
        else:
            print("No report ID found. Cannot delete from Firebase.")

cred = credentials.Certificate('../Account_management/credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def main():
    # Create a Com_Report instance
    com_report = Com_Report()

    # Set attributes
    com_report.set_community_name("Community A")
    com_report.set_leaderboard({"user1": 100, "user2": 200})
    com_report.set_current_month("July")
    com_report.set_current_year(2023)
    com_report.set_list_months(["January", "February", "March"])
    com_report.set_line_data([10, 20, 30, 40])
    com_report.set_pie_data({"data1": 50, "data2": 60})
    com_report.set_most_contributed("user2")
    com_report.set_activities(["activity1", "activity2", "activity3"])
    com_report.set_pie_label("label1")

    # Save to Firebase
    com_report.save_to_firebase()

    # Load from Firebase
    loaded_report_data = Com_Report.load_from_firebase(com_report.get_report_id())
    print("Loaded Report Data:")
    print(loaded_report_data)


if __name__ == "__main__":
    main()