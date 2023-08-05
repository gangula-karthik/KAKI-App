import logging
from flask import Flask, request, render_template, flash, get_flashed_messages, redirect, url_for, jsonify
import colorlog
from colorama import Fore
import datetime
import pyrebase
import sys
sys.path.append("Report_generation")
from Report_generation.Forms import CreateUserForm
from customer_support.ticket import *
from imageUploader import FirebaseStorageClient
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from Report_generation.report_class import Com_Report, Indi_Report, Trans_Report
from Report_generation.Admin_classes import *
from Report_generation.report_functions import get_all_reports, retrieve_report_name, retrieve_ByID
from Report_generation.report_functions import *
from Report_generation.retriving_data_functions import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_socketio import SocketIO, send
from collections import OrderedDict
from customer_support.comments import Comment
from flask import Flask, jsonify, request
from langchain import PromptTemplate, LLMChain
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import textwrap
import json

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]


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
app.secret_key = 'karthik123'
socketio = SocketIO(app)
current_user = 'leap'


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

@app.route('/', methods=['GET'])
def index():
    events = retreive_data_event()
    names = retreive_event_name(events)
    return render_template('/Report_generation/event_list.html', user_name=current_user,events = names)
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

# Customer support routes

template = """Question: {question}

Using this information about helpdesk tickets: {formatted_template}

Answer: Let's think step by step."""
prompt_template = PromptTemplate(template=template, input_variables=["question", "formatted_template"])

# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.6, "max_new_tokens": 2000}, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)



llm_chain = LLMChain(prompt=prompt_template, llm=falcon_llm)

async def generate_faqs(tickets):
    faqs = []

    async def generate_faq(ticket):
        subject = pyredb.child(f'tickets/{ticket}/subject').get().val()
        description = pyredb.child(f'tickets/{ticket}/descriptions').get().val()
        comments = pyredb.child(f'comments/').get().val()
        comments_text = '\n'.join(comments) if comments else ''

        formatted_template_data = f"Subject: {subject}\n\nDescription: {description}\n\nComments: {comments_text}"
        questions = [
            f"Could you elaborate on the issue reported in ticket {ticket}?",
            f"What is the current status of ticket {ticket}?",
            f"Who is currently handling ticket {ticket}?",
            f"What are the next steps planned for resolving ticket {ticket}?"
        ]

        for question in questions:
            formatted_prompt = {
                "question": question,
                "formatted_template": formatted_template_data
            }
            response = llm_chain.run(formatted_prompt)
            faqs.append({
                "question": question,
                "answer": response
            })

    await asyncio.gather(*(generate_faq(ticket) for ticket in tickets))

    return faqs



@app.route('/support_overview', methods=['GET'])
def customerOverview():

    tickets = pyredb.child('tickets').get().val()  
    faqs = asyncio.run(generate_faqs(tickets))


    messages = get_flashed_messages()
    return render_template('customer_support/support_overview.html', user_name=current_user, messages=messages, faqs=faqs)

@app.route('/user_chat', methods=['GET'])
def staffChat():
    return render_template('customer_support/user_chat.html', user_name=current_user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new_ticket', methods=['POST'])
def new_ticket():
    """
    FOR PS
    """
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


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

# customer support staff routes

@app.route('/supportStaffOverview', methods=['GET'])
def staffSupportOverview():
    return render_template('customer_support_staff/staffOverview.html', user_name=current_user)

@app.route('/ticketDashboard', methods=['GET'])
def staffTicketDashboard():
    return render_template('customer_support_staff/ticketManagement.html', user_name=current_user)

# report generation routes
@app.route('/Report_generation/Individual_report')
def Individual_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan","Feb","March","April","May","June"]
    leaderboard_data = [
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 36},
    {"name": "Player 3", "score": 72},
    {"name": "Player 4", "score": 60},
    {"name": "Player 5", "score": 69}
]
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
    return render_template('/Report_generation/Individual_report.html', leaderboard=leaderboard_data, user_name=current_user, current_month = month, line_data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths,neighbours_helped = '69', number_of_activities = '69')

@app.route('/Report_generation/Community_report')
def Community_report():
    now = datetime.datetime.now()
    month = str(now.strftime("%B"))
    current_year = str(now.year)
    ListMonths = ["Jan","Feb","March","April","May","June"]
    leaderboard_data = [
        {"name": "Player 1", "score": 100},
        {"name": "Player 2", "score": 36},
        {"name": "Player 3", "score": 72},
        {"name": "Player 4", "score": 60},
        {"name": "Player 5", "score": 69}
    ]
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
    return render_template('/Report_generation/Community_report.html', leaderboard=leaderboard_data, user_name=current_user, current_month = month, line_data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, most_contribute = 'Nameless', number_of_activities = '69')

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


@app.route('/event_lists', methods=['GET'])
def event_list():
    events = retreive_data_event()
    names = retreive_event_name(events)
    return render_template('/Report_generation/event_list.html', user_name=current_user,events = names)

@app.route('/Report_generation/Event_details.html/<report>', methods=['GET'])
def Event_details(report):
    events = retreive_data_event()
    details = retrieve_event_from_name(events, report)


    return render_template('/Report_generation/Event_details.html', user_name=current_user,details = details)

@app.route('/Report_generation/update.html/<event_name>', methods = ['GET', 'POST'])
def update(event_name):
    events = retreive_data_event()
    event_details = retrieve_event_from_name(events, event_name)
    update_user_form = CreateUserForm(request.form)
    return render_template('/Report_generation/update.html', user_name=current_user, form=update_user_form,event=event_details)

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

import datetime
@app.route('/Report_generation/general_report', methods=['GET'])
def general_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan", "Feb", "March", "April", "May", "June"]
    return render_template('/Report_generation/general_report.html', user_name=current_user,current_month = month, Total_community = 69, Total_users = 69, Total_number = 69,current_year=current_year,listMonths = ListMonths)

    
@app.route('/Report_generation/Transactions_report', methods=['GET'])
def Transactions_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan", "Feb", "March", "April", "May", "June"]
    total_count = total_count_transactions()
    total_cost = sum_cost_in_route()
    total_received = sum_retrieve_in_route()
    return render_template('/Report_generation/Transactions_report.html', user_name=current_user,current_month = month, Total_spent = total_cost, Total_received = total_received, Total_number = total_count,current_year=current_year,listMonths = ListMonths)

@app.route('/Report_generation/saved_reports',methods=['GET'])
def Saved_report():
    reports = get_all_reports()
    details = retrieve_report_name(reports)
    return render_template('/Report_generation/saved_reports.html', user_name=current_user, reports = details)

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
        pie_data = data['pie_data']
        most_contributed = data['most_contributed']
        activities = data['activities']
        pie_label = data['pie_label']

        return render_template('/Report_generation/Community_report.html', leaderboard = leaderboard, current_month = current_month,current_year = current_year, listMonths = listMonths,line_data=line_data,pie_data = pie_data,most_contributed=most_contributed,activities=activities,pie_label=pie_label)
    elif report_type == "Individual":
        leaderboard = data['leaderboard']
        current_month = data['current_month']
        current_year = data['current_year']
        listMonths = data['list_months']
        line_data = data['line_data']
        pie_data = data['pie_data']
        neighbours_helped = data['neighbours_helped']
        activities = data['activities']
        pie_label = data['pie_label']

        return render_template('/Report_generation/Individual_report.html',leaderboard = leaderboard, current_month = current_month,current_year = current_year, listMonths = listMonths,line_data=line_data,pie_data = pie_data,neighbours_helped=neighbours_helped,activities=activities,pie_label=pie_label)

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



@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):



    pyredb.child('products').child(product_id).remove()
    flash('Product has been deleted')
    return redirect(url_for('marketplace'))



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)