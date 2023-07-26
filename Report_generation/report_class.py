import firebase_admin
from firebase_admin import credentials
from firebase_admin import db





class Indi_Report:
    counter = 0
    def __init__(self):
        number = str(Trans_Report.counter + 1)
        report_id = 'I' + number
        self.__report_id__ = report_id
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__pieData__ = None
        self.__neighboursHelped__ = None
        self.__activities__ = None
        self.__pieLabel__ = None

    # Getter and setter methods for Indi_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def set_report_id(self, report_id):
        self.__report_id__ = report_id

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

    def get_neighbours_helped(self):
        return self.__neighboursHelped__

    def set_neighbours_helped(self, neighbours_helped):
        self.__neighboursHelped__ = neighbours_helped

    def get_activities(self):
        return self.__activities__

    def set_activities(self, activities):
        self.__activities__ = activities

    def get_pie_label(self):
        return self.__pieLabel__

    def set_pie_label(self, pie_label):
        self.__pieLabel__ = pie_label

    # Add getter and setter methods for other attributes as needed

    # Method to save Indi_Report to Firebase
    def save_to_firebase(self):
        report_data = {
            "Report_id": self.__report_id__,
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

        ref = db.reference("Users/Saved_report/Indi_report/")
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Indi_Report from Firebase using report_id
    @classmethod
    def load_from_firebase(cls, target_report_id):
        ref = db.reference("/Users/Saved_report/Indi_report")
        report_data = ref.get()
        for report_id, data in report_data.items():
            if data.get('Report_id') == target_report_id:
                return data

        return None

    # Method to update specific attribute of the report in Firebase
    def update_to_firebase(self, attribute_name, new_value):
        ref = db.reference("/Users/Saved_report/Indi_report")
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})

    def delete_from_firebase(self):
        if self.__report_id__:
            ref = db.reference("/Users/Saved_report/Indi_report")
            report_ref = ref.child(self.__report_id__)
            report_ref.delete()
        else:
            print("No report ID found. Cannot delete from Firebase.")




class Com_Report:
    counter = 0
    def __init__(self):
        number = str(Trans_Report.counter + 1)
        report_id = 'C' + number
        self.__report_id__ = report_id
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
            "Report_id": self.__report_id__,
            "leaderboard": self.__leaderboard__,
            "current_month": self.__CurrentMonth__,
            "current_year": self.__CurrentYear__,
            "listMonths": self.__listMonths__,
            "line_data": self.__lineData__,
            "pie_data": self.__pieData__,
            "most_contributed": self.__MostContributed__,
            "activities": self.__activities__,
            "pie_label": self.__pieLabel__,
        }

        ref = db.reference("/Users/Saved_report/Com_report")
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Com_Report from Firebase using report_id
    @classmethod
    def load_from_firebase(cls, target_report_id):
        ref = db.reference("/Users/Saved_report/Com_report")
        report_data = ref.get()
        for report_id, data in report_data.items():
            if data.get('Report_id') == target_report_id:
                return data

        return None

    # Method to update specific attribute of the report in Firebase
    def update_to_firebase(self, attribute_name, new_value):
        ref = db.reference("/Users/Saved_report/Com_report")
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})


    def delete_from_firebase(self):
        if self.__report_id__:
            ref = db.reference("/Users/Saved_report/Com_report")
            report_ref = ref.child(self.__report_id__)
            report_ref.delete()
        else:
            print("No report ID found. Cannot delete from Firebase.")


class Trans_Report:
    counter = 0

    def __init__(self):
        number = str(Trans_Report.counter + 1)
        report_id = 'T' + number
        self.__report_id__ = report_id
        self.__transactionDataIn__ = None
        self.__transactionDataOut__ = None
        self.__NoTransactionData__ = None
        self.__current_month__ = None
        self.__current_year__ = None
        self.__listMonths__ = None

    # Getter and setter methods for Trans_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def set_report_id(self, report_id):
        self.__report_id__ = report_id

    def get_transaction_data_in(self):
        return self.__transactionDataIn__

    def set_transaction_data_in(self, transaction_data_in):
        self.__transactionDataIn__ = transaction_data_in

    def get_transaction_data_out(self):
        return self.__transactionDataOut__

    def set_transaction_data_out(self, transaction_data_out):
        self.__transactionDataOut__ = transaction_data_out

    def get_no_transaction_data(self):
        return self.__NoTransactionData__

    def set_no_transaction_data(self, no_transaction_data):
        self.__NoTransactionData__ = no_transaction_data

    def get_current_month(self):
        return self.__current_month__

    def set_current_month(self, current_month):
        self.__current_month__ = current_month

    def get_current_year(self):
        return self.__current_year__

    def set_current_year(self, current_year):
        self.__current_year__ = current_year

    def get_list_months(self):
        return self.__listMonths__

    def set_list_months(self, list_months):
        self.__listMonths__ = list_months

    # Method to save Trans_Report to Firebase
    def save_to_firebase(self):
        report_data = {
            "Report_id": self.__report_id__,
            "transactionDataIn": self.__transactionDataIn__,
            "transactionDataOut": self.__transactionDataOut__,
            "NoTransactionData": self.__NoTransactionData__,
            "current_month": self.__current_month__,
            "current_year": self.__current_year__,
            "listMonths": self.__listMonths__,
        }

        ref = db.reference("/Users/Saved_report/Trans_report")
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Trans_Report from Firebase using report_id
    @classmethod
    def load_from_firebase(cls, target_report_id):
        ref = db.reference("/Users/Saved_report/Trans_report")
        report_data = ref.get()
        for report_id, data in report_data.items():
            if data.get('Report_id') == target_report_id:
                return data

        return None

    # Method to update specific attribute of the report in Firebase
    def update_to_firebase(self, attribute_name, new_value):
        ref = db.reference("/Users/Saved_report/Trans_report")
        report_ref = ref.child(self.__report_id__)
        report_ref.update({attribute_name: new_value})

    def delete_from_firebase(self):
        if self.__report_id__:
            ref = db.reference("/Users/Saved_report/Transaction_report")
            report_ref = ref.child(self.__report_id__)
            report_ref.delete()
        else:
            print("No report ID found. Cannot delete from Firebase.")






# cred = credentials.Certificate('../Account_management/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})
#
# # Assuming you have already initialized the Firebase SDK and set up the database reference (db)
#
# indi_report = Indi_Report()
# indi_report.set_leaderboard({"user1": 100, "user2": 200})
# indi_report.set_current_month("July")
# indi_report.set_current_year(2023)
# indi_report.set_list_months(["January", "February", "March"])
# indi_report.set_line_data([10, 20, 30, 40])
# indi_report.set_pie_data({"data1": 50, "data2": 60})
# indi_report.set_neighbours_helped({"neighbor1": 5, "neighbor2": 10})
# indi_report.set_activities(["activity1", "activity2", "activity3"])
# indi_report.set_pie_label("label1")
#
# # Save the Indi_Report to Firebase
# indi_report.save_to_firebase()
#
# # Load the Indi_Report from Firebase using the report_id
# report_id_to_load = indi_report.get_report_id()
# loaded_report_data = Indi_Report.load_from_firebase(report_id_to_load)
# print(loaded_report_data)


