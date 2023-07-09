from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

app = Flask(__name__)

cred = credentials.Certificate("Account_management/credentials.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('account_management/login.html')


# @app.route('/create_account',methods=['GET','POST'])
# def create_account():
#     if request.method == 'POST':
#         pwd0 = request.form['user_pwd0']
#         pwd1 = request.form['user_pwd1']
#         if pwd0 == pwd1:
#             email = request.form['user_email']
#             try:
#                 user = auth.create_user(
#                     email=email,
#                     password=pwd0
#                 )
#                 auth.send_email_verification(user.email)
#                 auth.generate_email_verification_link(user['idToken'])
#                 return render_template('account_management/verify_email.html')
#             except:
#                 existing_account = "An account with this email already exists."
#                 return render_template('account_management/login.html', exist_message=existing_account)
#     return render_template('account_management/login.html')


    #   except Exception as e:
    #             return "Error creating user: " + str(e)


# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.form.get('email')
#     password = request.form.get('password')

#     try:
#         user = auth.create_user(
#             email=email,
#             password=password
#         )
#         return "User created successfully: " + user.uid
#     except Exception as e:
#         return "Error creating user: " + str(e)

if __name__ == '__main__':
    app.run()