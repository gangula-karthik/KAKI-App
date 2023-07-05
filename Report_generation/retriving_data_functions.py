import firebase_admin
from firebase_admin import credentials, db


def initialize_firebase():
    # Replace 'path/to/your/serviceAccountKey.json' with the path to your Firebase Admin SDK credentials
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id.firebaseio.com'
    })


def extract_data_from_firebase(path, customer_key):
    result_list = []

    try:
        ref = db.reference(path)
        data = ref.get()

        if data:
            customer_data = data.get(customer_key)
            if customer_data:
                result_list.append(customer_data)
    except Exception as e:
        print(f"Error occurred while fetching data from Firebase: {e}")

    return result_list


def extract_data_from_firebase_attribute(path, attribute, value):
    result_list = []

    try:
        ref = db.reference(path)
        data = ref.get()

        if data:
            for key, value_dict in data.items():
                if attribute in value_dict and value_dict[attribute] == value:
                    result_list.append(value_dict)
    except Exception as e:
        print(f"Error occurred while fetching data from Firebase: {e}")

    return result_list


def extract_individual_with_highest_quantity(path):
    highest_quantity_individual = None
    highest_quantity = float('-inf')  # Initialize with negative infinity

    try:
        ref = db.reference(path)
        data = ref.get()

        if data:
            for key, value_dict in data.items():
                quantity = value_dict.get("quantity")
                if quantity is not None and quantity > highest_quantity:
                    highest_quantity = quantity
                    highest_quantity_individual = value_dict
    except Exception as e:
        print(f"Error occurred while fetching data from Firebase: {e}")

    return highest_quantity_individual


def extract_top_n_individuals_by_quantity(path, n):
    individuals = []

    try:
        ref = db.reference(path)
        data = ref.get()

        if data:
            sorted_data = sorted(data.values(), key=lambda x: x.get("quantity", 0), reverse=True)
            individuals = sorted_data[:n]
    except Exception as e:
        print(f"Error occurred while fetching data from Firebase: {e}")

    return individuals