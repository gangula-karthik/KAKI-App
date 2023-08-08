# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# cred = credentials.Certificate("../Account_management/credentials.json")
# firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})
#
#
# def count_instances_in_path(path = '/Events'):
#     data = db.reference(path).get()
#
#     if isinstance(data, dict):
#         return len(data)
#     elif isinstance(data, list):
#         return len(data)
#     else:
#         return 0
#
# if __name__ == "__main__":
#
#     instances_count = count_instances_in_path()
#     print(f"Number of instances in path '': {instances_count}")