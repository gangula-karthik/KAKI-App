import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime, timedelta
from calendar import month_abbr
import calendar
import pyrebase


# config = {
#     "apiKey": "AIzaSyBTdJ-q5cuHwkH7iZ9Np2fyFJEeCujN0Jg",
#     "authDomain": "kaki-db097.firebaseapp.com",
#     "projectId": "kaki-db097",
#     "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "storageBucket": "kaki-db097.appspot.com",
#     "messagingSenderId": "521940680838",
#     "appId": "1:521940680838:web:96e15f16f11bb306c91107",
#     "measurementId": "G-QMBGXFXJET"
# }
#
# firebase = pyrebase.initialize_app(config)
# pyredb = firebase.database()
# pyreauth = firebase.auth()
# pyrestorage = firebase.storage()

def initialize_firebase():
    # Replace 'path/to/your/serviceAccountKey.json' with the path to your Firebase Admin SDK credentials
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id.firebaseio.com'
    })


def extract_record_by_value(key, value_field, target_value, details_fields):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Query Firestore for the specific record
    records_ref = db.collection(key).where(value_field, '==', target_value).limit(1)
    records = records_ref.get()

    for record in records:
        record_data = record.to_dict()
        return record_data

    return None


def extract_last_12_months_values(collection_name, individual_id, value_field):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Get the current date and time
    current_date = datetime.now()

    # Create a dictionary to store the month-value mapping
    month_values = {}

    # Retrieve the values for the last 12 months
    for i in range(12):
        # Calculate the start and end dates for the month
        start_date = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*30)
        end_date = current_date.replace(day=1, hour=23, minute=59, second=59, microsecond=999) - timedelta(days=i*30)
        month_name = month_abbr[start_date.month]

        # Query Firestore for the values within the month for the individual
        records_ref = db.collection(collection_name).where('individual_id', '==', individual_id).where('timestamp', '>=', start_date).where('timestamp', '<=', end_date)
        records = records_ref.get()

        # Calculate the sum of the values for the month
        month_value = sum(record.get(value_field) for record in records)

        # Map the month to the value in the dictionary
        month_values[month_name] = month_value

    return month_values


def extract_top_record_by_value(collection_name, value_field, name_field):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the top record from Firestore
    records_ref = db.collection(collection_name).order_by(value_field, direction='DESCENDING').limit(1)
    records = records_ref.get()

    for record in records:
        record_data = record.to_dict()
        return record_data.get(name_field)

    return None


def extract_top_records(collection_name, value_field, details_fields, limit=5):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the top records from Firestore
    records_ref = db.collection(collection_name).order_by(value_field, direction='DESCENDING').limit(limit)
    records = records_ref.get()

    top_records = []
    for record in records:
        record_data = {}
        # Extract value field
        record_data[value_field] = record.get(value_field)
        # Extract details fields
        for field in details_fields:
            record_data[field] = record.get(field)

        top_records.append(record_data)

    return top_records

def retrieve_participation_count(event_id):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Retrieve the event document from Firestore
    event_ref = db.collection('events').document(event_id)
    event_doc = event_ref.get()

    # Check if the event document exists
    if event_doc.exists:
        # Retrieve the 'participation_count' field value
        participation_count = event_doc.get('participation_count')

        if participation_count is not None:
            return participation_count
        else:
            return 0  # Participation count not set for the event
    else:
        return 0  # Event document not found in Firestore

def get_last_six_months():
    today = datetime.now()
    last_six_months = []

    for i in range(6):
        last_six_months.insert(0, calendar.month_name[today.month])
        today -= timedelta(days=today.day)
        today -= timedelta(days=1)

    return last_six_months


def get_top_communities_for_specific_month_and_year(month, year, num_top):
    communities_data = db.reference("/CommunityPoints").get()

    community_points = {}

    for community, months_data in communities_data.items():
        if year in months_data and month in months_data.get(year, {}):
            total_points = months_data[year][month]["points"]
            community_points[community] = total_points

    # Sort communities by points in descending order
    sorted_communities = sorted(community_points.items(), key=lambda x: x[1], reverse=True)

    # Return the top 'num_top' communities
    top_communities = sorted_communities[:num_top]

    return top_communities

def get_community_data_from_firebase(community_name):
    community_ref = db.reference(f"/CommunityPoints/{community_name}")
    community_data = community_ref.get()

    if community_data is None:
        return {}  # Return an empty dictionary if no data found

    return community_data
def get_last_five_months_of_specified_year(community_name, year, current_month):
    community_data = get_community_data_from_firebase(community_name)  # Replace with Firebase data retrieval

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    result = []

    for i in range(5, -1, -1):
        month_index = (months.index(current_month) - i) % 12
        month = months[month_index]

        if year in community_data and month in community_data[year]:
            points = community_data[year][month]["points"]
        else:
            points = 0

        result.append(points)

    return result

def get_all_individuals():
    individuals_ref = db.reference("/IndividualPoints")
    individuals_data = individuals_ref.get()

    if individuals_data is None:
        return []  # Return an empty list if no individual data found

    return list(individuals_data.keys())

def get_individual_data_from_firebase(individual_name):
    individual_ref = db.reference(f"/IndividualPoints/{individual_name}")
    individual_data = individual_ref.get()

    if individual_data is None:
        return {}  # Return an empty dictionary if no data found

    return individual_data
def get_individual_points_for_month(individual_name, year, month):
    individual_data = get_individual_data_from_firebase(individual_name)  # Replace with Firebase data retrieval

    if year in individual_data and month in individual_data[year]:
        points = individual_data[year][month]["points"]
    else:
        points = 0

    return points


def get_top_individuals_by_points(year, month, community, limit=5):
    individuals_data = db.reference("/IndividualPoints").get()

    individual_points = {}

    for individual, months_data in individuals_data.items():
        if community and months_data.get("community") != community:
            continue  # Skip individuals not in the specified community

        if year in months_data and month in months_data.get(year, {}):
            total_points = months_data[year][month]["points"]
            individual_points[individual] = total_points

    # Sort individuals by points in descending order
    sorted_individuals = sorted(individual_points.items(), key=lambda x: x[1], reverse=True)

    # Return the top 'limit' individuals
    top_individuals = sorted_individuals[:limit]

    return top_individuals

def get_individual_points_over_past_months(individual_name, year, current_month):
    individual_data = get_individual_data_from_firebase(individual_name)  # Replace with Firebase data retrieval

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    result = []

    for i in range(5, -1, -1):
        month_index = (months.index(current_month) - i) % 12
        month = months[month_index]

        if year in individual_data and month in individual_data[year]:
            points = individual_data[year][month]["points"]
        else:
            points = 0

        result.append(points)

    return result

def get_individual_activities(individual_name, year, month):
    individual_data = get_individual_data_from_firebase(individual_name)  # Replace with Firebase data retrieval

    if year in individual_data and month in individual_data[year]:
        activities = individual_data[year][month]["activities"]
    else:
        activities = 0

    return activities

def get_individual_with_most_points_in_community(community, year, month):
    individuals_data = db.reference("/IndividualPoints").get()
    community_individuals = [individual for individual, data in individuals_data.items() if data.get("community") == community]

    max_points = 0
    top_individual = None

    for individual in community_individuals:
        if year in individuals_data[individual] and month in individuals_data[individual][year]:
            points = individuals_data[individual][year][month]["points"]
            if points > max_points:
                max_points = points
                top_individual = individual

    return top_individual


def count_transactions_past_6_months_for_buyer(year, month, buyer_name):
    transactions_data = db.reference("/TransactionsDummy").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    transaction_counts = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        count = 0

        if transactions_data:
            for transaction_key, transaction in transactions_data.items():
                if "year" in transaction and "month" in transaction and "buyer" in transaction:
                    if transaction["year"] == current_year and transaction["month"] == current_month and transaction[
                        "buyer"] == buyer_name:
                        count += 1

        transaction_counts.insert(0, count)  # Insert at the beginning to reverse the order

    return transaction_counts


def sum_product_costs_past_6_months_for_seller(year, month, seller_name):
    transactions_data = db.reference("/TransactionsDummy").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    product_cost_sum = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        cost_sum = 0

        if transactions_data:
            for transaction_key, transaction in transactions_data.items():
                if "year" in transaction and "month" in transaction and "seller" in transaction and "product_cost" in transaction:
                    if transaction["year"] == current_year and transaction["month"] == current_month and transaction[
                        "seller"] == seller_name:
                        cost_sum += transaction["product_cost"]

        product_cost_sum.insert(0, cost_sum)  # Insert at the beginning to reverse the order

    return product_cost_sum

def sum_product_costs_past_6_months_for_buyer(year, month, buyer_name):
    transactions_data = db.reference("/TransactionsDummy").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    product_cost_sum = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        cost_sum = 0

        if transactions_data:
            for transaction_key, transaction in transactions_data.items():
                if "year" in transaction and "month" in transaction and "buyer" in transaction and "product_cost" in transaction:
                    if transaction["year"] == current_year and transaction["month"] == current_month and transaction[
                        "buyer"] == buyer_name:
                        cost_sum += transaction["product_cost"]

        product_cost_sum.insert(0, cost_sum)  # Insert at the beginning to reverse the order

    return product_cost_sum

def count_transactions_past_6_months(year, month):
    transactions_data = db.reference("/TransactionsDummy").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    transaction_counts = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        count = 0

        if transactions_data:
            for transaction_key, transaction in transactions_data.items():
                if "year" in transaction and "month" in transaction:
                    if transaction["year"] == current_year and transaction["month"] == current_month:
                        count += 1

        transaction_counts.append(count)

    return transaction_counts

def count_events(path = '/Events'):
    data = db.reference(path).get()

    if isinstance(data, dict):
        return len(data)
    elif isinstance(data, list):
        return len(data)
    else:
        return 0
def count_signups_per_year_month(year, month):
    users_data = db.reference("/Users/Consumer").get()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    month_index = months.index(month)

    year_month_counts = []

    for i in range(6):
        current_month_index = (month_index - i) % 12
        current_month = months[current_month_index]
        current_year = year

        if current_month_index > month_index:
            current_year -= 1

        signups_count = 0

        if users_data:
            for user_key, user in users_data.items():
                if "year" in user and "month" in user:
                    if user["year"] == current_year and user["month"] == current_month:
                        signups_count += 1

        year_month_counts.insert(0, signups_count)  # Insert at the beginning to reverse the order

    return year_month_counts
