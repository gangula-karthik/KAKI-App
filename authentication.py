from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase

app = Flask(__name__)

cred = credentials.Certificate("Account_management/credentials.json")
firebase_admin.initialize_app(cred)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pwd']
        try:
            user = auth.get_user_by_email(email)
            if user.email_verified:
                auth_user = auth.sign_in_with_email_and_password(email, password)
                return render_template('template.html')
            else:
                verify_message = 'Please verify your account'
                return render_template('account_management/login.html', umessage=verify_message)
        except auth.AuthError as e:
            unsuccessful = 'Please check credentials'
            return render_template('account_management/login.html', umessage=unsuccessful)
    return render_template('account_management/login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['user_email']
        auth.generate_password_reset_link(email)
        print(auth.generate_password_reset_link(email))
        return render_template('account_management/login.html')
    return render_template('account_management/login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        pwd0 = request.form['user_pwd0']
        pwd1 = request.form['user_pwd1']
        if pwd0 == pwd1:
            email = request.form['user_email']
            try:
                user = auth.create_user(
                    email=email,
                    password=pwd0
                )
                # auth.generate_email_verification_link(user['idToken'])
                return render_template('account_management/veryify_email.html')
            except auth.EmailAlreadyExistsError:
                existing_account = "An account with this email already exists."
                return render_template('account_management/login.html', exist_message=existing_account)
    return render_template('account_management/login.html')


# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['user_email']
#     password = request.form['user_pwd']
#     try:
#         user = auth.get_user_by_email(email)
#         auth.verify_password(email, password)  # Verify the password entered
#         return render_template('template.html')
#     except auth.UserNotFoundError:
#         error_message = "Invalid email or password."
#         return render_template('account_management/login.html', error_message=error_message)
#     except ValueError:
#         error_message = "Invalid email or password."
#         return render_template('account_management/login.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)