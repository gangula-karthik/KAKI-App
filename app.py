import logging
from flask import Flask, request, render_template, flash, get_flashed_messages, redirect, url_for, jsonify , session ,redirect, abort
import colorlog
from colorama import Fore
from datetime import datetime
import pyrebase
import calendar
import sys
sys.path.append("Report_generation")
from Report_generation.Forms import CreateUserForm
from customer_support.ticket import *
from imageUploader import FirebaseStorageClient
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from Report_generation.report_class import Com_Report, Indi_Report, Trans_Report
from Report_generation.Admin_classes import *
from Report_generation.report_functions import get_all_reports, retrieve_report_name, retrieve_ByID
from Report_generation.report_functions import *
from Report_generation.retriving_data_functions import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import requests

from flask_socketio import SocketIO, send
from collections import OrderedDict
from customer_support.comments import Comment
from flask import Flask, jsonify, request
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from flask_executor import Executor
from customer_support.FAQ_worker import generate_faqs
from customer_support.kakiGPT import generate_answers
import time



config = {
    "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
}

cred = credentials.Certificate('Account_management/credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})


app = Flask(__name__)
executor = Executor(app)
app.secret_key = 'karthik123'
socketio = SocketIO(app)
current_user = 'Leap'
staffStatus = False


app.config['UPLOAD_FOLDER'] = "/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)-8s%(reset)s %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
    }
))

# @app.before_first_request
# def init_app():
#     app.logger.info("Starting app...")
#     app.logger.info(Fore.GREEN + """
                    
#     | | / / / _ \ | | / /_   _|
#     | |/ / / /_\ \| |/ /  | |  
#     |    \ |  _  ||    \  | |  
#     | |\  \| | | || |\  \_| |_ 
#     \_| \_/\_| |_/\_| \_/\___/ ver 1.1.0
    
#     A product by Team Rocket Dev 🚀
#     Software is lincensed under MIT License
#                 """)



#Account management Routes
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validate reCAPTCHA response
        recaptcha_response = request.form['g-recaptcha-response']
        secret_key = "6LcVAHgnAAAAADAjOy6d57YNiSnviQnkqJxuv9KG"  
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"

        data = {
            'secret': secret_key,
            'response': recaptcha_response
        }

        response = requests.post(captcha_url, data=data)
        result = response.json()

        if not result['success']:
            unsuccessful = 'Please complete the reCAPTCHA verification.'
            return render_template('account_management/login.html', umessage=unsuccessful)

        # Rest of your login logic (similar to your existing code)
        email = request.form['user_email']
        password = request.form['user_pwd']
        try:
            user = pyreauth.sign_in_with_email_and_password(email, password)
            # Get the Firebase token ID
            token_id = user['idToken']
            # Save the token ID in the session
            session['user_token'] = token_id

            firebase_user = auth.get_user(user['localId'])
            email_verified = firebase_user.email_verified
            if not email_verified:
                # Update user's custom claims to indicate pending email verification
                auth.set_custom_user_claims(user['localId'], {'emailVerified': False})

                # Send the email verification
                pyreauth.send_email_verification(user['idToken'])
                print("Verification email sent. Waiting for email verification...")
                # Wait until the email is verified
                while True:
                    firebase_user = auth.get_user(user['localId'])
                    email_verified = firebase_user.email_verified
                    if email_verified:
                        # Update user's custom claims to indicate email verification completed
                        auth.set_custom_user_claims(user['localId'], {'emailVerified': True})
                        print("Email verified.")
                        break
                    else:
                        print("Email not verified. Waiting...")
                        time.sleep(5)  # Add a 5-second delay before checking again
            else:
                print("Email already verified.")

            return redirect('/staff/users')
            # return redirect('/dashboard')
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

        # Use the UID as the key in the database to get the user data
        user_data = pyredb.child("Users").child("Consumer").child(uid).get().val()
        print(user_data)
        return render_template('account_management/update_usercred.html', user_data=user_data)
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

                session['user_token'] = user

                session['pwd'] = pwd0

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

        # Save the username in the session
        session['username'] = username

        # Retrieve the email from the session
        email = session.get('user_email', None)
        # Retrieve the token ID from the session
        token_id = session.get('user_token', None)  

        password = session.get('pwd', None)

        if email is None:
            return "User email not found. Please create an account first."

        if token_id is None:
            return "User token ID not found. Please log in first."
        # Add the "status" field with the value "User" to the data
        data = {
            "email": email,
            "name": name,
            "username": username,
            "birthdate": birthdate,
            "town": town,
            "status": "User"  # Add the "status" field with the value "User"
        }
        # Use the token ID as the key in the database
        pyredb.child("Users").child("Consumer").child(token_id).set(data)
        try:
            user = pyreauth.sign_in_with_email_and_password(email, password)
            # Get the Firebase token ID
            token_id = user['idToken']
            # Save the token ID in the session
            session['user_token'] = token_id

            firebase_user = auth.get_user(user['localId'])
            email_verified = firebase_user.email_verified
            if not email_verified:
                # Update user's custom claims to indicate pending email verification
                auth.set_custom_user_claims(user['localId'], {'emailVerified': False})

                # Send the email verification
                pyreauth.send_email_verification(user['idToken'])
                print("Verification email sent. Waiting for email verification...")
                # Wait until the email is verified
                while True:
                    firebase_user = auth.get_user(user['localId'])
                    email_verified = firebase_user.email_verified
                    if email_verified:
                        # Update user's custom claims to indicate email verification completed
                        auth.set_custom_user_claims(user['localId'], {'emailVerified': False})
                        session.pop('pwd',None)  
                        print("Email verified.")
                        break
                    else:
                        print("Email not verified. Waiting...")
                        time.sleep(5)  # Add a 5-second delay before checking again
            else:
                print("Email already verified.")
        except Exception as e:
            print(f"Authentication failed: {e}")
        return redirect('/staff/users')
        

@app.route('/update_user_cred', methods=['POST'])
def update_user_credentials():
    if 'user_token' in session:
        # Retrieve the token ID from the session
        token_id = session['user_token']

        # Use the token ID to get the user's UID from Firebase authentication
        user = pyreauth.get_account_info(token_id)
        uid = user['users'][0]['localId']

        # Get the updated data from the form
        name = request.form['fullName']
        email = request.form['eMail']
        username = request.form['username']
        birthdate = request.form['birthdate']
        town = request.form['town']

        # Update the user data in Firebase
        data = {
            "name": name,
            "email": email,
            "username": username,
            "birthdate": birthdate,
            "town": town
        }

        pyredb.child("Users").child("Consumer").child(uid).update(data)

        # Redirect to the dashboard with updated data
        return redirect('/dashboard')

    else:
        return "User token ID not found. Please log in first."


@app.route('/delete_account', methods=['POST'])
def delete_account():
    try:
        # Get the user's token ID from the session
        token_id = session.get('user_token', None)
        
        if token_id:
            session.pop('user_email', None)            
            # Delete the user from Firebase Authentication
            decoded_token = pyreauth.get_account_info(token_id)
            user_id = decoded_token['users'][0]['localId']
            auth.delete_user(user_id)

            # Delete user data from the Realtime Database (assuming the user's data is stored in 'Users/Consumer' node)
            pyredb.child("Users").child("Consumer").child(user_id).remove()
            
            # After deleting the account and data, redirect the user to the login page
            return redirect('/')
        else:
            # Handle the case where the token_id is not available in the session
            return redirect('/error-page')
    except Exception as e:
        # Handle any errors that may occur during account deletion
        print('Error deleting account:', str(e))
        # You can choose to show an error message or redirect the user to an error page
        return redirect('/error-page')


@app.route('/staff/users')
def show_all_users():
    try:
        # Get all user data from the Realtime Database (assuming the user's data is stored in 'Users/Consumer' node)
        all_users_data = pyredb.child("Users").child("Consumer").get().val()

        return render_template('account_management/show_all_users.html', all_users_data=all_users_data)
    except Exception as e:
        # Handle any errors that may occur
        print('Error:', str(e))
        # You can choose to show an error message or redirect the user to an error page
        return redirect('/error-page')


@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        # Get the user_id and user_data from the request's JSON payload
        request_data = request.get_json()
        user_id = request_data.get('user_id')
        user_data = request_data.get('user_data')

        # Update the user data in Firebase
        pyredb.child("Users").child("Consumer").child(user_id).update(user_data)

        # Return a success message (if needed)
        return "User data updated successfully"
    except Exception as e:
        # Handle any errors that may occur during the update process
        print('Error updating user data:', str(e))
        # You can choose to show an error message or return an error response
        return "Error updating user data", 500


@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        data = request.get_json()
        user_id = data['user_id']

        # Delete the user data from the database
        auth.delete_user(user_id)
        pyredb.child("Users").child("Consumer").child(user_id).remove()
        pyrebase.child("Users").child("Consumer").child(user_id).child('birthdate-placeholder').remove()
        pyrebase.child("Users").child("Consumer").child(user_id).child('town-placeholder').remove()
        pyrebase.child("Users").child("Consumer").child(user_id).child('username-placeholder').remove()

        return "User data deleted successfully!"
    except Exception as e:
        # Handle any errors that may occur
        print('Error deleting user data:', str(e))
        return "Error deleting user data."

#End for Account Management Routes

@app.route('/', methods=['GET'])
def eventTest():
    events = retreive_data_event()
    names = retreive_event_name(events)
    if staffStatus: 
        return render_template('/Report_generation/event_list.html', user_name=current_user,events = names, is_staff=True)
    else:
        return render_template('/Report_generation/event_list.html', user_name=current_user,events = names, is_staff=False)
# Changed the template to my own so that i can see the layout


@app.route('/home', methods=['GET'])
def home():
    return render_template('homefeed.html', user_name=current_user)

@app.route('/myposts', methods=['GET'])
def mypost():
    return render_template('homefeed.html', user_name=current_user)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    return render_template('homefeed.html', user_name=current_user)

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('customer_support/user_chat.html', user_name=current_user)

@app.route('/noticeboard', methods=['GET'])
def noticeboard():
    return render_template('notices.html', user_name=current_user)

@app.route('/friend_request', methods=['GET'])
def friendRequest():
    return render_template('friend_request.html', user_name=current_user)


# customer support routes

# Global variable to keep track of the future
future = None

@app.route('/support_overview', methods=['GET'])
def customerOverview():
    global future
    try:
        tickets = pyredb.child('tickets').get().val()
    except Exception as e:
        logging.error(f'Error retrieving tickets: {e}')
        flash('An error occurred while retrieving tickets, please try again later', 'error')
        tickets = None
      
    if future is None:
        future = executor.submit(generate_faqs)

    if future.done():
        faqs = future.result()
        messages = get_flashed_messages()
        return render_template('customer_support/support_overview.html', user_name=current_user, messages=messages, faqs=faqs)
    else:
        return render_template('customer_support/loading.html'), 202



@app.route('/faq_status', methods=['GET'])
def faq_status():
    if future.done():
        faqs = future.result()
        return jsonify({'status': 'done', 'faqs': faqs})
    else:
        return jsonify({'status': 'pending'})




@app.route('/user_chat')
def listTickets():
    all_tickets = pyredb.child("tickets").get().val() or {}
    return render_template('customer_support/user_chat.html', tickets=all_tickets, messages={})


@app.route('/user_chat/<ticket_id>', methods=['GET'])
def staffChat(ticket_id):
    all_tickets = pyredb.child("messages").get().val() or {}
    ticket_messages = all_tickets.get(ticket_id, {})
    return render_template('customer_support/user_chat.html', tickets=all_tickets, messages=ticket_messages, ticket_id=ticket_id, username=current_user)



@app.route('/send_message/<ticket_id>/<username>', methods=['POST'])
def send_message(ticket_id, username):
    print("Ticket ID:", ticket_id)
    print("Username:", username)
    message_content = request.form.get('message')
    data = {
        "user": current_user,  
        "staff_id": "456",
        "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        "content": message_content
    }
    pyredb.child(f"messages/{ticket_id}").push(data) 
    return redirect(url_for('staffChat', ticket_id=ticket_id))





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/new_ticket', methods=['POST'])
def new_ticket():
    subject = request.form.get('subject')
    description = request.form.get('description')
    topic = request.form.get('topic')
    file = request.files.get('file')

    ticket = Ticket(current_user, subject, description, topic)

    if file:
        # get the file name, this doesn't include the path
        filename = secure_filename(file.filename)
        
        # upload the file to firebase storage
        firebase_storage_client = FirebaseStorageClient(config, "ticket_images")
        firebase_storage_client.upload(file, filename) # passing file object directly
        url = firebase_storage_client.get_url(filename)
        
        # create new ticket and add image url
        ticket.addImages(url)

    flash('Ticket has been submitted 🚀')
    
    messages = get_flashed_messages()  # Get the flashed messages
    return redirect(url_for('customerOverview'))

@app.route('/update_ticket/<ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    # Retrieve the existing ticket
    ticket = [i for i in ticketRetrieval() if i['ticket_id'] == ticket_id][0]
    if not ticket:
        flash('Ticket not found')
        return redirect(url_for('customerOverview'))
    
    # Get the new data from the form
    subject = request.form.get('subject')
    description = request.form.get('description')
    topic = request.form.get('topic')
    file = request.files.get('file')

    updateSubject(ticket_id, subject)
    updateDescriptions(ticket_id, description)
    updateTopic(ticket_id, topic)

    if file:
        # get the file name, this doesn't include the path
        filename = secure_filename(file.filename)
        
        # upload the file to firebase storage
        firebase_storage_client = FirebaseStorageClient(config, "ticket_images")
        firebase_storage_client.upload(file, filename) # passing file object directly
        url = firebase_storage_client.get_url(filename)
        
        # update ticket image url
        ticket.updateImages(url)

    flash('Ticket has been updated 🚀')
    
    messages = get_flashed_messages()  # Get the flashed messages
    return redirect(url_for('myTickets'))

@app.route('/ticket_search', methods=['GET'])
def search():
    query = request.args.get('query')
    return redirect(url_for('userTickets', query=query, user_name=current_user))

def ticketRetrieval():
    allTickets = pyredb.child("tickets").get()
    try:
        tickets = [i.val() for i in allTickets.each()]
    except:
        tickets = []
    return tickets


@app.route('/get_ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = [i for i in ticketRetrieval() if i['ticket_id'] == ticket_id]
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    return ticket[0]



@app.route('/delete_ticket/<ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    AllowedIds = [i["ticket_id"] for i in ticketRetrieval() if i['user_id'] == current_user]
    if ticket_id not in AllowedIds:
        return jsonify({'error': 'System Error, Try again'}), 404
    deleteTicket(ticket_id)
    referrer_url = request.referrer
    return redirect(referrer_url)


@app.route('/my_tickets', methods=['GET'])
def myTickets():
    tickets = ticketRetrieval()
    myTickets = [i for i in tickets if i['user_id'] == current_user]
    return render_template('customer_support/my_tickets.html', user_name=current_user,data=myTickets)

@app.route('/user_tickets', methods=['GET'])
def userTickets():
    query = request.args.get('query')
    if query:
        tickets = semanticSearch(query)
    else:
        tickets = ticketRetrieval()
    return render_template('customer_support/ticket_discussion.html', user_name=current_user, data=tickets)


def getComments(): 
    comment = pyredb.child("comments").get().val()
    return comment

@app.route('/user_tickets/<ticket_ID>', methods=['GET', 'POST'])
def ticketComments(ticket_ID):
    tickets = ticketRetrieval()
    if tickets is None:
        return "Error: tickets could not be retrieved."

    ticket = next((i for i in tickets if i['ticket_id'] == ticket_ID), None)
    if ticket is None:
        return f"Error: No ticket with ID {ticket_ID} could be found."

    commList = []

    comms = getComments()
    if comms is not None:
        commList = [(id, comment) for id, comment in comms.items() if comment['ticket_id'] == ticket_ID]
    return render_template('customer_support/ticket_comments.html', user_name=current_user, data=ticket, comments=commList)


@app.route('/user_tickets/add_comment/<ticket_ID>', methods=['POST'])
def set_comment(ticket_ID):
    comment = request.form.get('commentText')
    comment_date = datetime.datetime.now().strftime("%Y-%m-%d")
    comment_by = current_user
    comment_data = {
        "comment": comment,
        "ticket_id": ticket_ID,
        "date": comment_date,
        "comment_by": comment_by
    }
    comment_req = Comment().add_comment(ticket_ID, comment, comment_date, comment_by)
    if comment_req == 200: 
        flash('Comment has been added 🚀', 'success')

    return redirect(url_for('ticketComments', ticket_ID=ticket_ID))

@app.route('/user_tickets/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(comment_id):
    pyredb.child("comments").child(comment_id).remove()
    flash('Comment has been deleted 🗑️', 'success')
    return redirect(request.referrer)

@app.route('/update_comment/<comment_id>', methods=['POST'])
def update_comment(comment_id):
    new_comment_text = request.form.get('commentText') 

    comment = pyredb.child("comments").child(comment_id).get()
    if not comment.val():
        flash('Comment not found!', 'error')
        return redirect(request.referrer)

    pyredb.child("comments").child(comment_id).update({"comment": new_comment_text})
    
    flash('Comment has been updated!', 'success')
    return redirect(request.referrer)

def background_task_bot_message(user_message):
    time.sleep(2)
    bot_response = generate_answers(user_message)
    return bot_response
    


@app.route('/kakigpt', methods=['GET', 'POST'])
def kakiGPT():
    chat_history = session.get('chat_history', [])

    if request.method == 'POST':
        user_message = request.form.get('user_message')
        chat_history.append({'type': 'user', 'message': user_message})

        future = executor.submit(background_task_bot_message, user_message)
        bot_response = future.result()

        chat_history.append({'type': 'bot', 'message': bot_response})
        session['chat_history'] = chat_history

        return jsonify({'bot_response': bot_response})

    return render_template('customer_support/kakigpt.html', user_name=current_user, chat_history=chat_history)



# customer support staff routes

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.route('/supportStaffOverview', methods=['GET'])
def staffSupportOverview():
    if staffStatus:
        return render_template('customer_support_staff/staffOverview.html', user_name=current_user)
    else: 
        return abort(403)

@app.route('/ticketDashboard', methods=['GET'])
def staffTicketDashboard():
    if staffStatus:
        return render_template('customer_support_staff/ticketManagement.html', user_name=current_user)
    else: 
        return abort(403)

# report generation routes
@app.route('/Report_generation/Individual_report')
def Individual_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = get_last_six_months()
    leaderboard_data = [
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 36},
    {"name": "Player 3", "score": 72},
    {"name": "Player 4", "score": 60},
    {"name": "Player 5", "score": 69}
]
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
    if staffStatus == 'user':
        return render_template('/Report_generation/Individual_report.html', leaderboard=leaderboard_data, user_name=current_user, current_month = month, line_data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths,neighbours_helped = '69', number_of_activities = '69', is_staff=False)
    else:
        return render_template('/Report_generation/Individual_report.html', leaderboard=leaderboard_data,
                               user_name=current_user, current_month=month, line_data=[5, 6, 7, 8, 9, 10],
                               current_year=current_year, listMonths=ListMonths, neighbours_helped='69',
                               number_of_activities='69', is_staff=True)

import datetime
@app.route('/Report_generation/Community_report')
def Community_report():
    now = datetime.datetime.now()
    month = str(now.strftime("%B"))
    current_year = str(now.year)
    ListMonths = get_last_six_months()
    leaderboard_data = [
        {"name": "Player 1", "score": 100},
        {"name": "Player 2", "score": 36},
        {"name": "Player 3", "score": 72},
        {"name": "Player 4", "score": 60},
        {"name": "Player 5", "score": 69}
    ]
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
    if staffStatus == 'user':
        return render_template('/Report_generation/Community_report.html', leaderboard=leaderboard_data, user_name=current_user, current_month = month, line_data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, most_contributed = 'Nameless', number_of_activities = '69', is_staff = False)
    else:
        return render_template('/Report_generation/Community_report.html', leaderboard=leaderboard_data, user_name=current_user, current_month = month, line_data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, most_contributed = 'Nameless', number_of_activities = '69', is_staff = True)


@app.route('/save_data/com', methods=['POST'])
def save_data_com():
    data = request.json
    report = get_com()
    check = check_existing(report,data)

    logging.info(f"Received data: {data}")
    logging.info(f"Existing report: {report}")
    logging.info(f"Check existing report result: {check}")
    if check == True:
             return jsonify({'message': 'Report already saved'})
    else:
        # Create a Com_Report instance and set the attributes from the received data
        report_c = Com_Report()
        report_c.set_leaderboard(data['leaderboard'])
        report_c.set_current_month(data['current_month'])
        report_c.set_current_year(data['current_year'])
        report_c.set_list_months(data['listMonths'])
        report_c.set_line_data(data['line_data'])
        report_c.set_most_contributed(data['most_contributed'])
        report_c.set_activities(data['number_of_activities'])
        # Add other attributes as needed

        # Save the report to Firebase using the class method
        report_c.save_to_firebase()

        # Return a response to indicate success (you can customize this based on your needs)
        return jsonify({"message": "Data saved successfully!"})



@app.route('/save_data/indi', methods=['POST'])
def save_data_indi():

    data = request.json
    report = get_indi()
    check = check_existing(report,data)

    logging.info(f"Received data: {data}")
    logging.info(f"Existing report: {report}")
    logging.info(f"Check existing report result: {check}")
    if check == True:
             return jsonify({'message': 'Report already saved'})
    else:
        # Create a Com_Report instance and set the attributes from the received data
        report_i = Indi_Report()
        report_i.set_leaderboard(data['leaderboard'])
        report_i.set_current_month(data['current_month'])
        report_i.set_current_year(data['current_year'])
        report_i.set_list_months(data['listMonths'])
        report_i.set_line_data(data['line_data'])
        report_i.set_neighbours_helped(data['neighbours_helped'])
        report_i.set_activities(data['number_of_activities'])

        # Add other attributes as needed

        # Save the report to Firebase using the class method
        report_i.save_to_firebase()

        # Return a response to indicate success (you can customize this based on your needs)
        return jsonify({"message": "Data saved successfully!"})

@app.route('/save_data/trans', methods=['POST'])
def save_data_trans():


    data = request.json
    report = get_trans()
    check = check_existing(report,data)

    logging.info(f"Received data: {data}")
    logging.info(f"Existing report: {report}")
    logging.info(f"Check existing report result: {check}")
    if check == True:
             return jsonify({'message': 'Report already saved'})
    else:
        # Create a Com_Report instance and set the attributes from the received data
        report_trans = Trans_Report()
        report_trans.set_current_month(data['current_month'])
        report_trans.set_current_year(data['current_year'])
        report_trans.set_list_months(data['listMonths'])
        report_trans.set_Total_spent(data['Total_spent'])
        report_trans.set_Total_received(data['Total_received'])
        report_trans.set_no_transaction_data(data['Total_number'])
        # Add other attributes as needed

        # Save the report to Firebase using the class method
        report_trans.save_to_firebase()

        # Return a response to indicate success (you can customize this based on your needs)
        return jsonify({"message": "Data saved successfully!"})

@app.route('/Report_generation/Transactions_report', methods=['GET'])
def Transactions_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = get_last_six_months()
    # total_count = total_count_transactions()
    # total_cost = sum_cost_in_route()
    # total_received = sum_retrieve_in_route()
    if staffStatus == 'user':
        return render_template('/Report_generation/Transactions_report.html', user_name=current_user,current_month = month, Total_spent = [6,9,6,9,6,9], Total_received = [6,9,6,9,6,9], Total_number = [6,9,6,9,6,9],current_year=current_year,listMonths = ListMonths,is_staff=False)
    else:
        return render_template('/Report_generation/Transactions_report.html', user_name=current_user,current_month = month, Total_spent = [6,9,6,9,6,9], Total_received = [6,9,6,9,6,9], Total_number = [6,9,6,9,6,9],current_year=current_year,listMonths = ListMonths,is_staff=True)

@app.route('/Report_generation/saved_reports',methods=['GET'])
def Saved_report():
    reports = get_all_reports()
    details = retrieve_report_name(reports)
    if staffStatus == 'user':
        return render_template('/Report_generation/saved_reports.html', user_name=current_user, reports = details, is_staff=False)

@app.route('/Report_generation/<string:report_type>/<string:Report_id>', methods=['GET'])
def view_report(report_type,Report_id):
    report = get_all_reports()
    data = retrieve_ByID(report,Report_id)
    if report_type == "Community":
        leaderboard = data['leaderboard']
        current_month = data['current_month']
        current_year = data['current_year']
        listMonths = data['listMonths']
        line_data = data['line_data']
        number_of_activities = data['activities']
        most_contributed = data['most_contributed']


        return render_template('/Report_generation/Community_report.html', leaderboard = leaderboard, current_month = current_month,current_year = current_year, listMonths = listMonths,line_data=line_data,number_of_activities = number_of_activities,most_contributed=most_contributed)
    elif report_type == "Individual":
        leaderboard = data['leaderboard']
        current_month = data['current_month']
        current_year = data['current_year']
        listMonths = data['list_months']
        line_data = data['line_data']
        neighbours_helped = data['neighbours_helped']
        activities = data['activities']


        return render_template('/Report_generation/Individual_report.html',leaderboard = leaderboard, current_month = current_month,current_year = current_year, listMonths = listMonths,line_data=line_data,neighbours_helped=neighbours_helped,number_of_activities=activities)

    elif report_type == "Transaction":
        current_month = data['current_month']
        current_year = data['current_year']
        list_month = data['listMonths']
        total_spent = data['Total_spent']
        total_received = data['Total_received']
        total_number = data['NoTransactionData']

        return render_template('/Report_generation/Transactions_report.html',current_month=current_month,current_year=current_year,listMonths=list_month,Total_spent=total_spent,Total_received=total_received,Total_number=total_number)

@app.route('/delete/data', methods=['POST'])
def delete_report():
    report_id = str(request.json)
    report = get_all_reports()
    details = retrieve_ByID(report, report_id)
    report_type = details['report_type']


    if report_type == "Community":
        delete_Com_from_firebase(report_id)
        return jsonify({"status": "success"})


    elif report_type == "Individual":
        delete_Indi_from_firebase(report_id)
        return jsonify({"status": "success"})


    elif report_type == "Transaction":
        delete_Trans_from_firebase(report_id)
        return jsonify({"status": "success"})
@app.route('/event_lists', methods=['GET'])
def event_list():
    events = retreive_data_event()
    names = retreive_event_name(events)
    if staffStatus == 'staff':
        return render_template('/Report_generation/event_list.html', user_name=current_user,events = names, is_staff=True)
    else:
        return render_template('/Report_generation/event_list.html', user_name=current_user,events = names, is_staff=False)

@app.route('/Report_generation/Event_details.html/<report>', methods=['GET'])
def Event_details(report):
    events = retreive_data_event()
    details = retrieve_event_from_name(events, report)

    if staffStatus == 'staff':
        return render_template('/Report_generation/Event_details.html', user_name=current_user,details = details,is_staff=True)
    else:
        return render_template('/Report_generation/Event_details.html', user_name=current_user, details=details,
                               is_staff=False)


@app.route('/Report_generation/update.html/<event_name>', methods = ['GET', 'POST'])
def update(event_name):
    events = retreive_data_event()
    event_details = retrieve_event_from_name(events, event_name)
    update_user_form = CreateUserForm(request.form)
    if staffStatus == 'staff':
        return render_template('/Report_generation/update.html', user_name=current_user, form=update_user_form,event=event_details, is_staff=True)
    else:
        return render_template('/Report_generation/update.html', user_name=current_user, form=update_user_form,
                               event=event_details, is_staff=False)


@app.route('/updateEvent', methods=['POST'])
def update_event():
    data = request.get_json()

    event_name = data.get('event_name')
    original = extract_event_by_name(event_name)

    try:
        if original is None:
            return jsonify({'message': 'Event not found'})

        for key, value in data.items():
            if key in original and original[key] != value:
                original[key] = value

        # Get a reference to the "Events" location in the database
        ref = db.reference("Events")

        # Update the existing data with the new data
        ref.child(event_name).update(original)

        return jsonify({'message': 'Updated'})
    except Exception as e:
        return jsonify({'message': 'Error during update'})


@app.route('/Report_generation/general_report', methods=['GET'])
def general_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = get_last_six_months()

    if staffStatus == 'staff':
        return render_template('/Report_generation/general_report.html', user_name=current_user,current_month = month, Total_community = [6,9,6,9,6,9], Total_users = [6,9,6,9,6,9], Total_numberT = [6,9,6,9,6,9],current_year=current_year,listMonths = ListMonths, is_staff=True)
    else:
        return render_template('/Report_generation/general_report.html', user_name=current_user,current_month = month, Total_community = [6,9,6,9,6,9], Total_users = [6,9,6,9,6,9], Total_numberT = [6,9,6,9,6,9],current_year=current_year,listMonths = ListMonths, is_staff=False)

    




#Transaction handling routes
@app.route('/transaction_handling/MyProducts/<int:product_id>')
def MyProducts(product_id):
    products = [
        {
            'title': 'Fantastic Book',
            'description': ' This is a fantastic book that will take you on an unforgettable journey through its captivating plot,keeping you turning the pages until the very end.',
            'price': 14.99,
            'seller': 'Jane Doe',
            'rating': 4.7,
            'condition': 'Like New',
            'image': 'book.jpg',
        },
        {
            'title': 'Vintage Bicycle',
            'description': ' This vintage bicycle is a true gem for bike enthusiasts. Its classic design and sturdy build make it perfect for leisurely rides in the neighborhood.',
            'price': 199.99,
            'seller': 'John Smith',
            'rating': 4.5,
            'condition': 'Used',
            'image': 'bicycle.jpg',
        },
        {
            'title': 'Garden Tools',
            'description': 'This garden tools set is perfect for anyone with a green thumb. It includes everything you need to tend to your garden and grow beautiful plants.',
            'price': 49.99,
            'seller': 'Mary Johnson',
            'rating': 4.8,
            'condition': 'New',
            'image': 'gardentools.jpg',
        },
        {
            'title': 'Digital Camera',
            'description': 'This digital camera is perfect for capturing all your special moments. Its high-resolution sensor and advanced features ensure stunning photos and videos.',
            'price': 299.99,
            'seller': 'Michael Brown',
            'rating': 4.6,
            'condition': 'Used',
            'image': 'digitalcamera.jpg',
        },
        {
            'title': 'Skateboard',
            'description': 'This skateboard is perfect for beginners and experienced riders alike. Its durable construction and smooth wheels ensure a fun and safe ride.',
            'price': 49.99,
            'seller': 'Robert Johnson',
            'rating': 4.4,
            'condition': 'Used',
            'image': 'skateboard.jpg',
        },
        {
            'title': 'Cookware Set',
            'description': 'This cookware set is a must-have for any aspiring chef. It includes high-quality pots, pans, and utensils to help you create delicious meals.',
            'price': 79.99,
            'seller': 'Emily Lee',
            'rating': 4.9,
            'condition': 'Like New',
            'image': 'Cookware.jpg',
        },
        {
            'title': 'Acoustic Guitar',
            'description': 'This acoustic guitar is perfect for music enthusiasts and aspiring musicians. Its rich tones and comfortable playability make it a joy to play.',
            'price': 199.99,
            'seller': 'Sarah Brown',
            'rating': 4.3,
            'condition': 'Used',
            'image': 'acousticguitar.jpg',
        },
        {
            'title': 'Original Painting',
            'description': 'This original painting is a masterpiece that will add beauty and elegance to any home. Its stunning colors and intricate details are truly captivating.',
            'price': 499.99,
            'seller': 'William Doe',
            'rating': 4.2,
            'condition': 'Like New',
            'image': 'Paining.jpg',
        },
        {
            'title': 'Headphones',
            'description': 'These wireless headphones deliver an immersive audio experience. With noise-canceling technology and long battery life, they are perfect for music lovers on the go.',
            'price': 99.99,
            'seller': 'Lisa Johnson',
            'rating': 4.7,
            'condition': 'Used',
            'image': 'wirelessheadphones.jpg',
        },

        # Add more product dictionaries here for other products
    ]
   # product = next((p for p in products if p['id'] == product_id), None)
    #if product:
    return render_template('/transaction_handling/MyProducts.html', user_name=current_user)
    #return "Product not found"

@app.route('/transaction_handling/marketplace')
def marketplace():
    allProducts = pyredb.child("products").get().val()

    products = [(id, productInfo) for id, productInfo in allProducts.items()]
    # for i in allProducts.each():
    #     res.append(i.val())
    
    return render_template('/transaction_handling/marketplace.html', products = products, user_name = current_user)



@app.route('/handle_modal_submission', methods=['POST'])
def handle_modal_submission():
    # Access the form data from the request object
    product_name = request.form.get('productName')
    # product_image = request.files['productImage']
    product_description = request.form.get('productDescription')
    product_price = request.form.get('productPrice')
    product_condition = request.form.get('productCondition')

    data = {"product_name": product_name, "product_description": product_description, "product_price": product_price, "product_condition": product_condition, "seller": current_user}
    pyredb.child("products").push(data)

    # Redirect to a page or return a response
    return redirect(url_for('marketplace'))

@app.route('/transaction_get_value')
def show_all_products():
    try:
        # Get all user data from the Realtime Database (assuming the user's data is stored in 'Users/Consumer' node)
        all_users_data = pyredb.child("products").get().val()

        return render_template('marketplace', all_users_data=all_users_data)
    except Exception as e:
        # Handle any errors that may occur
        print('Error:', str(e))
        # You can choose to show an error message or redirect the user to an error page
        return redirect('/error-page')



@app.route('/update_product/<product_id>', methods=['POST'])
def update_product(product_id):
    # Retrieve form data
    product_name = request.form.get('updatedProductName')
    product_description = request.form.get('updatedProductDescription')
    product_price = request.form.get('updatedProductPrice')
    product_condition = request.form.get('updatedProductCondition')

    # Construct the data dictionarys
    data = {
        "product_name": product_name,
        "product_description": product_description,
        "product_price": product_price,
        "product_condition": product_condition,
        "seller": current_user  # Assuming current_user is a global or session variable
    }

    print(data)

    # Update the product in Firebase
    pyredb.child(f"products/{product_id}").update(data)

    return redirect(url_for('marketplace'))
    
    

@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):



    pyredb.child('products').child(product_id).remove()
    flash('Product has been deleted')
    return redirect(url_for('marketplace'))



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)