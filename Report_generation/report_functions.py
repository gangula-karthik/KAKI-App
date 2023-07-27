from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db

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