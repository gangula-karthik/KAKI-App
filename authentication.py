from flask import Flask, render_template, request , session ,redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase


app = Flask(__name__)
app.secret_key = 'who420is420in12paris'

cred = credentials.Certificate("Account_management/credentials.json")
firebase_admin.initialize_app(cred)

config = {
    "apiKey": "AIzaSyBTdJ-q5cuHwkH7iZ9Np2fyFJEeCujN0Jg",
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
    "messagingSenderId": "521940680838",
    "appId": "1:521940680838:web:96e15f16f11bb306c91107",
    "measurementId": "G-QMBGXFXJET"
}

firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pwd']
        try:
            user = pyreauth.sign_in_with_email_and_password(email, password)
            # Get the Firebase token ID
            token_id = user['idToken']
            # Save the token ID in the session
            session['user_token'] = token_id

            return redirect('/dashboard')
        except:
            unsuccessful = 'Please check your credentials'
            return render_template('account_management/login.html', umessage=unsuccessful)
    return render_template('account_management/login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_token' in session:
        # Retrieve the token ID from the session
        token_id = session['user_token']

        # Use the token ID to get the user's UID from Firebase authentication
        user = pyreauth.get_account_info(token_id)

        uid = user['users'][0]['localId']
        
        print(f'user: {user}')
        print(uid)

        # Use the UID as the key in the database to get the user data
        user_data = pyredb.child("Users").child("Consumer").child(uid).get().val()
        print(user_data)
        return render_template('account_management/dashboard.html', user_data=user_data)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    # Clear the session on logout
    session.pop('user_email', None)
    return redirect('/')


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
                # Save the email in the session
                session['user_email'] = email

                # Get the Firebase token ID (use user.uid instead of user['idToken'])
                token_id = user.uid
                # Save the token ID in the session
                session['user_token'] = token_id

                return render_template('account_management/user_cred.html')

            except auth.EmailAlreadyExistsError:
                existing_account = "An account with this email already exists."
                return render_template('account_management/login.html', exist_message=existing_account)
    return render_template('account_management/login.html')


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    user_email = request.form.get('user_email')
    try:
        pyreauth.send_password_reset_email(user_email)
        return 'Password reset email sent successfully.'
    except:
        r_email = 'Error sending password reset email'
        return render_template('account_management/forget_password.html', exist_message=r_email)
    


@app.route('/add_user_credentials', methods=['GET', 'POST'])
def add_user_credentials():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        birthdate = request.form['birthdate']
        town = request.form['town']

        # Retrieve the email from the session
        email = session.get('user_email', None)

        # Retrieve the token ID from the session
        token_id = session.get('user_token', None)

        if email is None:
            return "User email not found. Please create an account first."

        if token_id is None:
            return "User token ID not found. Please log in first."

        data = {
            "email": email,  # Include the email in the data to be stored
            "name": name,
            "username": username,
            "birthdate": birthdate,
            "town": town
        }

        # Use the token ID as the key in the database
        pyredb.child("Users").child("Consumer").child(token_id).set(data)
        return "Data added successfully to Firebase!"
        
# @app.route('/update_user_credentials', methods=['GET', 'POST'])
# def update_user_credentials():
#     if request.method == 'POST':
#         name = request.form['name']
#         username = request.form['username']
#         birthdate = request.form['birthdate']
#         town = request.form['town']

#         # Retrieve the email from the session
#         email = session.get('user_email', None)

#         # Retrieve the token ID from the session
#         token_id = session.get('user_token', None)

#         if token_id is None:
#             return "User token ID not found. Please log in first."

#         if email is None:
#             return "User email not found. Please create an account first."

#         data = {
#             "email": email,  # Include the email in the data to be stored
#             "name": name,
#             "username": username,
#             "birthdate": birthdate,
#             "town": town
#         }

#         pyredb.child("Users").child("Consumer").child(token_id).set(data)
#         return "Data updated successfully to Firebase!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)