import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("Account_management/credentials.json")

firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

email = input('Enter email: ')
password = input('Enter password: ')

# user = auth.get_user_by_email(email)
# try:
#     user = auth.get_user_by_email(email)
    
#     verified_user = auth.verify_password(email=email, password=password)

#     if user.uid == verified_user.uid:
#         email_verified = user.email_verified
#         print(f"Email verified: {email_verified}")
#     else:
#         print("Invalid email or password.")

# except:
#     print("Authentication failed:")


user = auth.create_user(
    email=email,
    password=password,
)


# verification_link = auth.generate_email_verification_link(email)

print("User created successfully:", user.uid)

# print('email veriifcation:', verification_link)
