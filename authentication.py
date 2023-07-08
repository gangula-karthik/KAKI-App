from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

app = Flask(__name__)

cred = credentials.Certificate("Login/credentials.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return "User created successfully: " + user.uid
    except Exception as e:
        return "Error creating user: " + str(e)

if __name__ == '__main__':
    app.run()