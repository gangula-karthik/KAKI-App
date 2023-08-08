# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# cred = credentials.Certificate("../Account_management/credentials.json")
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})
#
#
# def insert_dummy_individual_points():
#     dummy_data = [
#         {
#             "name": "Emily Williams",
#             "community": "bishan_toa_payoh",
#             "points": {
#                 "2023": {
#                     "August": {"points": 130, "activities": 12},
#                     "July": {"points": 120, "activities": 10},
#                     "June": {"points": 110, "activities": 9},
#                     "May": {"points": 100, "activities": 11},
#                     "April": {"points": 90, "activities": 8},
#                 },
#             }
#         },
#         {
#             "name": "Daniel Brown",
#             "community": "bishan_toa_payoh",
#             "points": {
#                 "2023": {
#                     "August": {"points": 120, "activities": 11},
#                     "July": {"points": 110, "activities": 13},
#                     "June": {"points": 100, "activities": 10},
#                     "May": {"points": 90, "activities": 12},
#                     "April": {"points": 80, "activities": 9},
#                 },
#             }
#         },
#         {
#             "name": "John Doe",
#             "community": "bishan_toa_payoh",
#             "points": {
#                 "2023": {
#                     "August": {"points": 150, "activities": 10},
#                     "July": {"points": 140, "activities": 12},
#                     "June": {"points": 130, "activities": 15},
#                     "May": {"points": 120, "activities": 8},
#                     "April": {"points": 110, "activities": 11},
#                 },
#             }
#         },
#         {
#             "name": "Jane Smith",
#             "community": "bishan_toa_payoh",
#             "points": {
#                 "2023": {
#                     "August": {"points": 120, "activities": 8},
#                     "July": {"points": 110, "activities": 10},
#                     "June": {"points": 100, "activities": 7},
#                     "May": {"points": 90, "activities": 9},
#                     "April": {"points": 80, "activities": 6},
#                 },
#             }
#         },
#         {
#             "name": "Michael Johnson",
#             "community": "bishan_toa_payoh",
#             "points": {
#                 "2023": {
#                     "August": {"points": 140, "activities": 9},
#                     "July": {"points": 130, "activities": 11},
#                     "June": {"points": 120, "activities": 13},
#                     "May": {"points": 110, "activities": 10},
#                     "April": {"points": 100, "activities": 12},
#                 },
#             }
#         },
#         # Add more individuals and data here...
#     ]
#
#     for entry in dummy_data:
#         individual_name = entry["name"]
#         individual_community = entry["community"]
#         individual_data = entry["points"]
#         individual_data["community"] = individual_community  # Add the community column
#
#         individual_ref = db.reference(f"/IndividualPoints/{individual_name}")
#         individual_ref.set(individual_data)
#
#
#
# insert_dummy_individual_points()
#
# def get_individual_with_most_points_in_community(community, year, month):
#     individuals_data = db.reference("/IndividualPoints").get()
#     community_individuals = [individual for individual, data in individuals_data.items() if data.get("community") == community]
#
#     max_points = 0
#     top_individual = None
#
#     for individual in community_individuals:
#         if year in individuals_data[individual] and month in individuals_data[individual][year]:
#             points = individuals_data[individual][year][month]["points"]
#             if points > max_points:
#                 max_points = points
#                 top_individual = individual
#
#     return top_individual
#
# # Other functions and Firebase initialization...
#
# if __name__ == "__main__":
#     community = "bishan_toa_payoh"
#     year = "2023"
#     month = "August"
#     top_individual = get_individual_with_most_points_in_community(community, year, month)
#     if top_individual:
#         print(f"The individual with the most points in {community} for {month} {year} is {top_individual}.")
#     else:
#         print(f"No data found for {community} in {month} {year}.")
