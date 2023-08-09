from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify


# cred = credentials.Certificate('../Account_management/credentials.json')
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def get_all_reports(name):
    reports = {}

    categories = ["Transactions", "Individual", "Community"]

    try:
        reports_ref_trans = db.reference(f'/Users//Saved_report/{name}/Transactions')
        reports_snapshot_t = reports_ref_trans.get()
        reports.update(reports_snapshot_t)
    except:
        pass

    try:

        reports_ref_indi = db.reference(f'/Users//Saved_report/{name}/Individual')
        reports_snapshot_i = reports_ref_indi.get()
        reports.update(reports_snapshot_i)
    except:
        pass

    try:
        reports_ref_com = db.reference(f'/Users//Saved_report/{name}/Community')
        reports_snapshot_c = reports_ref_com.get()
        reports.update(reports_snapshot_c)

    except:
        pass

    return reports

def get_trans(name):
    reports = {}
    reports_ref_trans = db.reference(f'/Users//Saved_report/{name}/Transactions')
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
def get_indi(name):
    reports = {}
    reports_ref_trans = db.reference(f'/Users//Saved_report/{name}/Individual')
    reports_snapshot_t = reports_ref_trans.get()

    if reports_snapshot_t:
        # Merge the data from reports_snapshot_t into the reports dictionary
        for key, value in reports_snapshot_t.items():
            reports[key] = value

    return reports

def get_com(name):
    reports = {}
    reports_ref_trans = db.reference(f'/Users//Saved_report/{name}/Community')
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

def delete_Trans_from_firebase(report_id,name):
    if report_id:
        ref = db.reference(f'/Users//Saved_report/{name}/Transactions')
        report_data = ref.get()

        for report_key, data in report_data.items():
            if data.get('Report_id') == report_id:
                ref.child(report_key).delete()
                return True

    return False

def delete_Indi_from_firebase(report_id,name):
    if report_id:
        ref = db.reference(f'/Users//Saved_report/{name}/Individual')
        report_data = ref.get()

        for report_key, data in report_data.items():
            if data.get('Report_id') == report_id:
                ref.child(report_key).delete()
                return True

    return False

def delete_Com_from_firebase(report_id,name):
    if report_id:
        ref = db.reference(f'/Users//Saved_report/{name}/Community')
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
    ref = db.reference("Events")
    event_ref = ref.child(event_name)
    event_snapshot = event_ref.get()
    return event_snapshot

def update_event(event_obj, new_values):
    attributes_to_update = [
        'event_name',
        'venue',
        'event_date',
        'time',
        'overall_in_charge',
        'dateposted',
        'event_location',
        'event_description',
        'community',

    ]

    for attribute in attributes_to_update:
        if attribute in new_values:
            setattr(event_obj, attribute, new_values[attribute])

    # Assuming you have a method to update the event in the database (e.g., update_to_database)
    event_obj.update_to_database()


def total_count_transactions():
    # Get a reference to the Firestore database
    ref = db.reference("/products")

    # Reference the collection


    # Get the number of documents in the collection
    query_result = ref.get()
    if query_result == None:
        return 0
    else:
        count = len(query_result)

    return count

def sum_cost_in_route():
    # Get a reference to the Firestore database
    ref = db.reference("/products")

    list_items = ref.get()

    # Calculate the sum of the 'cost' column
    total_cost = 0
    for item in list_items:
        inst = list_items[item]

        mon = float(inst['product_price'])


        total_cost += mon

    return total_cost

def sum_retrieve_in_route():
    # Get a reference to the Firestore database
    ref = db.reference("/products")

    list_items = ref.get()

    # Calculate the sum of the 'cost' column
    total_cost = 0
    for item in list_items:
        inst = list_items[item]
        if inst['seller']=='leap':

            mon = float(inst['product_price'])
            total_cost += mon
        else:
            continue

    return total_cost

def sort_by_individual_points(top_n):
    # Get a reference to the Firestore database
    ref = db.reference("/this is the route to the individuals")

    list_items = ref.get()

    # Sort the items in descending order based on 'product_price' (cost)
    sorted_items = sorted(list_items.values(), key=lambda x: float(x['this is the name of the column of the points']), reverse=True)

    # Return the top products based on the desired number (top_n)
    return sorted_items[:top_n]


def get_top_communities(num_top):
    communities_data = db.reference("/CommunityPoints").get()

    community_points = {}

    for community, months_data in communities_data.items():
        total_points = sum(month_data["points"] for month_data in months_data.values())
        community_points[community] = total_points

    # Sort communities by total points in descending order
    sorted_communities = sorted(community_points.items(), key=lambda x: x[1], reverse=True)

    # Return the top 'num_top' communities
    top_communities = sorted_communities[:num_top]

    return top_communities



