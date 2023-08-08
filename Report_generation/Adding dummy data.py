# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# cred = credentials.Certificate("../Account_management/credentials.json")
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})
#
#
# def insert_dummy_community_points():
#     dummy_data = {
#         "bishan_toa_payoh": {
#             "2023": {
#                 "August": {"points": 150},
#             },
#         },
#         "aljunied_hougang": {
#             "2023": {
#                 "August": {"points": 120},
#             },
#         },
#         "woodlands": {
#             "2023": {
#                 "August": {"points": 130},
#             },
#         },
#         "jurong_east": {
#             "2023": {
#                 "August": {"points": 140},
#             },
#         },
#         "yishun": {
#             "2023": {
#                 "August": {"points": 110},
#             },
#         },
#         # Add more communities and data here...
#     }
#
#     for community_name, community_data in dummy_data.items():
#         community_ref = db.reference(f"/CommunityPoints/{community_name}")
#         community_ref.set(community_data)
#
#
# if __name__ == "__main__":
#     insert_dummy_community_points()
#
#
# def get_top_communities_for_specific_month_and_year(month, year, num_top):
#     communities_data = db.reference("/CommunityPoints").get()
#
#     community_points = {}
#
#     for community, months_data in communities_data.items():
#         if year in months_data and month in months_data.get(year, {}):
#             total_points = months_data[year][month]["points"]
#             community_points[community] = total_points
#
#     # Sort communities by points in descending order
#     sorted_communities = sorted(community_points.items(), key=lambda x: x[1], reverse=True)
#
#     # Return the top 'num_top' communities
#     top_communities = sorted_communities[:num_top]
#
#     return top_communities
#
# print(get_top_communities_for_specific_month_and_year('August','2023',5))
