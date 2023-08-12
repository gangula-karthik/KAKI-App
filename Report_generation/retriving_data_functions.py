import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime, timedelta
from calendar import month_abbr
import calendar
import pyrebase


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
        return {} 

    return community_data
def get_last_five_months_of_specified_year(community_name, year, current_month):
    community_data = get_community_data_from_firebase(community_name)  

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
        return []  

    return list(individuals_data.keys())

def get_individual_data_from_firebase(individual_name):
    individual_ref = db.reference(f"/IndividualPoints/{individual_name}")
    individual_data = individual_ref.get()

    if individual_data is None:
        return {}  

    return individual_data
def get_individual_points_for_month(individual_name, year, month):
    individual_data = get_individual_data_from_firebase(individual_name)  

    if year in individual_data and month in individual_data[year]:
        points = individual_data[year][month]["points"]
    else:
        points = 0

    return points


def get_top_individuals_by_points(year, month, limit=5):
    individuals_data = db.reference("/IndividualPoints").get()

    individual_points = {}

    for individual, data in individuals_data.items():
        if year in data and month in data.get(year, {}):
            total_points = data[year][month]["points"]
            individual_points[individual] = total_points

   
    sorted_individuals = sorted(individual_points.items(), key=lambda x: x[1], reverse=True)

    
    top_individuals = sorted_individuals[:limit]

    return top_individuals

def get_individual_points_over_past_months(individual_name, year, current_month):
    individual_data = get_individual_data_from_firebase(individual_name)  

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
    individual_data = get_individual_data_from_firebase(individual_name)  

    if year in individual_data and month in individual_data[year]:
        activities = individual_data[year][month]["activities"]
    else:
        activities = 0

    return activities


def get_individual_with_most_points_in_community(community, year, month):
    individuals_data = db.reference("/IndividualPoints").get()

    if not individuals_data:
        print("No data found for individuals.")
        return None

    community_individuals = [individual for individual, data in individuals_data.items() if
                             data.get("community") == community]

    if not community_individuals:

        return "No one in the community has points yet. Be the first."

    max_points = 0
    top_individual = None

    for individual in community_individuals:
        if year in individuals_data[individual] and month in individuals_data[individual][year]:
            points = individuals_data[individual][year][month]["points"]
            print(f"Individual: {individual}, Points: {points}")
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

        transaction_counts.insert(0, count)

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

        product_cost_sum.insert(0, cost_sum)  

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

        product_cost_sum.insert(0, cost_sum) 

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

def count_events_com(community,path='/Events', ):
    data = db.reference(path).get()
    if community:
        print(data)
        filtered_data = [event[1] for event in data.items() if event[1]['community'] == community]
        return len(filtered_data)
    else:
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

        year_month_counts.insert(0, signups_count) 

    return year_month_counts
