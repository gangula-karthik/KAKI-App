from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify


# cred = credentials.Certificate('../Account_management/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def get_all_reports():
    reports = {}

    categories = ["Transactions", "Individual", "Community"]

    try:
        reports_ref_trans = db.reference("/Users/Saved_report/Transactions")
        reports_snapshot_t = reports_ref_trans.get()
        reports.update(reports_snapshot_t)
    except:
        pass

    try:

        reports_ref_indi = db.reference("/Users/Saved_report/Individual")
        reports_snapshot_i = reports_ref_indi.get()
        reports.update(reports_snapshot_i)
    except:
        pass

    try:
        reports_ref_com = db.reference("/Users/Saved_report/Community")
        reports_snapshot_c = reports_ref_com.get()
        reports.update(reports_snapshot_c)

    except:
        pass

    return reports

def get_trans():
    reports = {}
    reports_ref_trans = db.reference("/Users/Saved_report/Transactions")
    reports_snapshot_t = reports_ref_trans.get()

    if reports_snapshot_t:
        # Merge the data from reports_snapshot_t into the reports dictionary
        for key, value in reports_snapshot_t.items():
            reports[key] = value

    return reports

# data ={'NoTransactionData': [5, 6, 7, 8, 9, 10], 'Report_id': 'T1', 'Total_received': [5, 6, 7, 8, 9, 10], 'Total_spent': [5, 6, 7, 8, 9, 10], 'current_month': 'July', 'current_year': '2023', 'listMonths': ['Jan', 'Feb', 'March', 'April', 'May', 'June'], 'report_type': 'Transaction'}
# list1 =get_trans()
# for i in list1:
#     if data['current_year']  == list1[i]['current_year'] and data['current_month'] == list1[i]['current_month']:
#         print('True')
# Use combination of cuurent moneth and year along with record type
def get_indi():
    reports = {}
    reports_ref_trans = db.reference("/Users/Saved_report/Individual")
    reports_snapshot_t = reports_ref_trans.get()

    if reports_snapshot_t:
        # Merge the data from reports_snapshot_t into the reports dictionary
        for key, value in reports_snapshot_t.items():
            reports[key] = value

    return reports

def get_com():
    reports = {}
    reports_ref_trans = db.reference("/Users/Saved_report/Community")
    reports_snapshot_t = reports_ref_trans.get()

    if reports_snapshot_t:
        # Merge the data from reports_snapshot_t into the reports dictionary
        for key, value in reports_snapshot_t.items():
            reports[key] = value

    return reports

def check_existing(report,data):
    if len(report) == 0:
        return False

    for item in report.values():
        if data['current_year'] == item['current_year'] and data['current_month'] == item['current_month']:
            return True

    return False

def retrieve_report_name(dictionary):
    names = []
    for i in dictionary:
        Report_id = dictionary[i]["Report_id"]
        year = dictionary[i]["current_year"]
        month = dictionary[i]["current_month"]
        type_r = dictionary[i]["report_type"]
        name = type_r+ ' ' + year +' ' + month
        report_type = dictionary[i]["report_type"]
        names.append({"name": name, "report_type": report_type, "Report_id": Report_id})

    return names

def retrieve_ByID(dictionary, target):
    for i in dictionary:
        if dictionary[i]["Report_id"] == target:
            return dictionary[i]
        else:
            continue
    return 'error'


# item = retrieve_ByID(get_all_reports(),'T5')

def delete_Trans_from_firebase(report_id):
    if report_id:
        ref = db.reference("/Users/Saved_report/Transactions")
        report_data = ref.get()

        for report_key, data in report_data.items():
            if data.get('Report_id') == report_id:
                ref.child(report_key).delete()
                return True

    return False

def delete_Indi_from_firebase(report_id):
    if report_id:
        ref = db.reference("/Users/Saved_report/Individual")
        report_data = ref.get()

        for report_key, data in report_data.items():
            if data.get('Report_id') == report_id:
                ref.child(report_key).delete()
                return True

    return False

def delete_Com_from_firebase(report_id):
    if report_id:
        ref = db.reference("/Users/Saved_report/Community")
        report_data = ref.get()

        for report_key, data in report_data.items():
            if data.get('Report_id') == report_id:
                ref.child(report_key).delete()
                return True

    return False
def retreive_data_event():
    reports = {}
    reports_ref_trans = db.reference("/Events")
    reports_snapshot_t = reports_ref_trans.get()

    if reports_snapshot_t:
        # Merge the data from reports_snapshot_t into the reports dictionary
        for key, value in reports_snapshot_t.items():
            reports[key] = value

    return reports

def retreive_event_name(dictionary):
    names = []
    for event_data in dictionary.values():
        names.append(event_data['event_name'])
    return names

def retrieve_event_from_name(dictionary, target):
    for i in dictionary:
        if dictionary[i]["event_name"] == target:
            return dictionary[i]
        else:
            continue
    return 'error'

def extract_event_by_name(event_name):
    try:
        # Get a reference to the "Events" location in the database
        ref = db.reference("Events")

        # Retrieve the event data with the given event_name
        event_data = ref.child(event_name).get()

        # If the event with the given event_name is not found, return None
        if event_data is None:
            return None

        return event_data

    except Exception as e:
        print("Error occurred:", str(e))
        return None

def update_event(event_obj, new_values):
    attributes_to_update = [
        'venue',
        'event_date',
        'time',
        'overall_in_charge',
        'dateposted',
        'event_location',
        'event_description'
    ]

    for attribute in attributes_to_update:
        if attribute in new_values:
            setattr(event_obj, attribute, new_values[attribute])

    # Assuming you have a method to update the event in the database (e.g., update_to_database)
    event_obj.update_to_database()

