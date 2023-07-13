import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("Account_management/credentials.json")

firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})

email = input('Enter email: ')
password = input('Enter password: ')

# user = auth.create_user(
#     email=email,
#     password=password,
#     email_verified=False  # Set email verification status to False initially
# )

try:
    user = auth.get_user_by_email(email)
    verified_user = auth.verify_password(email=email, password=password)
    auth.generate_password_reset_link

    if user.uid == verified_user.uid:
        email_verified = user.email_verified
        print(f"Email verified: {email_verified}")
    else:
        print("Invalid email or password.")

except auth.AuthError as e:
    print("Authentication failed:", e)


# verification_link = auth.generate_email_verification_link(email)

# # print("User created successfully:", user.uid)

# print('email veriifcation:', verification_link)
