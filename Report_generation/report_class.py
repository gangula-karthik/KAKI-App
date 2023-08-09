import firebase_admin
from firebase_admin import credentials
from firebase_admin import db





class Indi_Report:
    counter = 0
    def __init__(self):
        Trans_Report.counter += 1
        number = str()
        report_id = 'I' + number
        self.__report_id__ = report_id
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__neighboursHelped__ = None
        self.__activities__ = None
        self.__type__ =  'Individual'

    # Getter and setter methods for Indi_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def get_type(self):
        return 'Individual'

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


    def get_neighbours_helped(self):
        return self.__neighboursHelped__

    def set_neighbours_helped(self, neighbours_helped):
        self.__neighboursHelped__ = neighbours_helped

    def get_activities(self):
        return self.__activities__

    def set_activities(self, activities):
        self.__activities__ = activities



    # Add getter and setter methods for other attributes as needed

    # Method to save Indi_Report to Firebase
    def save_to_firebase(self,name):
        report_data = {
            "Report_id": self.__report_id__,
            "leaderboard": self.__leaderboard__,
            "current_month": self.__CurrentMonth__,
            "current_year": self.__CurrentYear__,
            "list_months": self.__listMonths__,
            "line_data": self.__lineData__,

            "neighbours_helped": self.__neighboursHelped__,
            "activities": self.__activities__,

            "report_type": 'Individual',

        }

        ref = db.reference(f'/Users//Saved_report/{name}/Individual')
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Indi_Report from Firebase using report_id
    # @classmethod
    # def load_from_firebase(cls, target_report_id,name):
    #     ref = db.reference(f'/Users//Saved_report/{name}/Individual')
    #     report_data = ref.get()
    #     for report_id, data in report_data.items():
    #         if data.get('Report_id') == target_report_id:
    #             return data
    #
    #     return None
    #
    # # Method to update specific attribute of the report in Firebase
    # def update_to_firebase(self, attribute_name, new_value,name):
    #     ref = db.reference(f'/Users//Saved_report/{name}/Individual')
    #     report_ref = ref.child(self.__report_id__)
    #     report_ref.update({attribute_name: new_value})

    def delete_from_firebase(self,name):
        if self.__report_id__:
            ref = db.reference(f'/Users//Saved_report/{name}/Individual')
            report_data = ref.get()

            for report_id, data in report_data.items():
                if data.get('Report_id') == self.__report_id__:
                    ref.child(report_id).delete()
                    return True

        return False




class Com_Report:
    counter = 0
    def __init__(self):
        Trans_Report.counter += 1
        number = str(Trans_Report.counter)
        report_id = 'C' + number
        self.__report_id__ = report_id
        self.__leaderboard__ = None
        self.__CurrentMonth__ = None
        self.__CurrentYear__ = None
        self.__listMonths__ = None
        self.__lineData__ = None
        self.__MostContributed__ = None
        self.__activities__ = None
        self.__type__ =  'Community'

    # Getter and setter methods for Com_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def get_type(self):
        return 'Community'

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



    def get_most_contributed(self):
        return self.__MostContributed__

    def set_most_contributed(self, most_contributed):
        self.__MostContributed__ = most_contributed

    def get_activities(self):
        return self.__activities__

    def set_activities(self, activities):
        self.__activities__ = activities



    # Add getter and setter methods for other attributes as needed

    # Method to save Com_Report to Firebase
    def save_to_firebase(self,name):
        report_data = {
            "Report_id": self.__report_id__,
            "leaderboard": self.__leaderboard__,
            "current_month": self.__CurrentMonth__,
            "current_year": self.__CurrentYear__,
            "listMonths": self.__listMonths__,
            "line_data": self.__lineData__,

            "most_contributed": self.__MostContributed__,
            "activities": self.__activities__,

            "report_type": 'Community',
        }

        ref = db.reference(f'/Users//Saved_report/{name}/Community')
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Com_Report from Firebase using report_id
    # @classmethod
    # def load_from_firebase(cls, target_report_id):
    #     ref = db.reference(f'/Users//Saved_report/{name}/Community')
    #     report_data = ref.get()
    #     for report_id, data in report_data.items():
    #         if data.get('Report_id') == target_report_id:
    #             return data
    #
    #     return None

    # Method to update specific attribute of the report in Firebase
    # def update_to_firebase(self, attribute_name, new_value):
    #     ref = db.reference(f'/Users//Saved_report/{name}/Community')
    #     report_ref = ref.child(self.__report_id__)
    #     report_ref.update({attribute_name: new_value})


    def delete_from_firebase(self,name):
        if self.__report_id__:
            ref = db.reference(f'/Users//Saved_report/{name}/Community')
            report_data = ref.get()

            for report_id, data in report_data.items():
                if data.get('Report_id') == self.__report_id__:
                    ref.child(report_id).delete()
                    return True

        return False


class Trans_Report:
    counter = 0

    def __init__(self):
        Trans_Report.counter += 1
        number = str(Trans_Report.counter)
        report_id = 'T' + number
        self.__report_id__ = report_id
        self.__Total_received__ = None
        self.__Total_spent__ = None
        self.__NoTransactionData__ = None
        self.__current_month__ = None
        self.__current_year__ = None
        self.__listMonths__ = None
        self.__type__ = 'Transactions'

    # Getter and setter methods for Trans_Report attributes
    def get_report_id(self):
        return self.__report_id__

    def get_type(self):
        return 'Transactions'

    def set_report_id(self, report_id):
        self.__report_id__ = report_id

    def get_Total_received(self):
        return self.__Total_received__

    def set_Total_received(self, transaction_data_in):
        self.__Total_received__ = transaction_data_in

    def get_Total_spent(self):
        return self.__Total_spent__

    def set_Total_spent(self, transaction_data_out):
        self.__Total_spent__ = transaction_data_out

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
    def save_to_firebase(self,name):
        report_data = {
            "Report_id": self.__report_id__,
            "Total_spent": self.__Total_spent__,
            "Total_received": self.__Total_received__,
            "NoTransactionData": self.__NoTransactionData__,
            "current_month": self.__current_month__,
            "current_year": self.__current_year__,
            "listMonths": self.__listMonths__,
            "report_type": 'Transactions',
        }

        ref = db.reference(f'/Users//Saved_report/{name}/Transactions')
        new_report_ref = ref.push()
        new_report_ref.set(report_data)

    # Method to load Trans_Report from Firebase using report_id
    # @classmethod
    # def load_from_firebase(cls, target_report_id):
    #     ref = db.reference(f'/Users//Saved_report/{name}/Transactions')
    #     report_data = ref.get()
    #     for report_id, data in report_data.items():
    #         if data.get('Report_id') == target_report_id:
    #             return data
    #
    #     return None
    #
    # # Method to update specific attribute of the report in Firebase
    # def update_to_firebase(self, attribute_name, new_value):
    #     ref = db.reference("f'/Users//Saved_report/{name}/Transactions'")
    #     report_ref = ref.child(self.__report_id__)
    #     report_ref.update({attribute_name: new_value})

    def delete_from_firebase(self,name):
        if self.__report_id__:
            ref = db.reference(f'/Users//Saved_report/{name}/Transactions')
            report_data = ref.get()

            for report_id, data in report_data.items():
                if data.get('Report_id') == self.__report_id__:
                    ref.child(report_id).delete()
                    return True

        return False






# cred = credentials.Certificate('../Account_management/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})




