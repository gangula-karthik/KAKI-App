import logging
from flask import Flask, request, render_template
import colorlog
from colorama import Fore
import datetime
import sys
sys.path.append("Report_generation")
from Report_generation.Forms import CreateUserForm




app = Flask(__name__)

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

@app.before_first_request
def init_app():
    app.logger.info("Starting app...")
    app.logger.info(Fore.GREEN + """
                    
    | | / / / _ \ | | / /_   _|
    | |/ / / /_\ \| |/ /  | |  
    |    \ |  _  ||    \  | |  
    | |\  \| | | || |\  \_| |_ 
    \_| \_/\_| |_/\_| \_/\___/ ver 1.1.0
    
    A product by Team Rocket Dev 🚀
    Software is lincensed under MIT License
                """)

@app.route('/', methods=['GET'])
def index():
    details = {
        'event_name': 'Sample Event',
        'event_date': '2023-07-30',
        'event_description': 'This is a sample event description.',
        'venue': 'Sample Venue',
        'time': '12:00 PM',
        'overall_in_charge': 'John Doe',
        'dateposted': '2023-07-23',
    }


    return render_template('/Report_generation/Event_details.html', name="Sheldon",details = details)
# Changed the template to my own so that i can see the layout

@app.route('/home', methods=['GET'])
def home():
    return render_template('homefeed.html', name="Sheldon")

@app.route('/myposts', methods=['GET'])
def mypost():
    return render_template('homefeed.html', name="Sheldon")

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    return render_template('homefeed.html', name="Sheldon")

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('customer_support/user_chat.html', name="Sheldon")

@app.route('/noticeboard', methods=['GET'])
def noticeboard():
    return render_template('notices.html', name="Sheldon")

@app.route('/friend_request', methods=['GET'])
def friendRequest():
    return render_template('friend_request.html', name="Sheldon")

# Customer support routes
@app.route('/support_overview', methods=['GET'])
def customerOverview():
    return render_template('customer_support/support_overview.html', name="Sheldon")

@app.route('/user_chat', methods=['GET'])
def staffChat():
    return render_template('customer_support/user_chat.html', name="Sheldon")


@app.route('/my_tickets', methods=['GET'])
def myTickets():
    return render_template('customer_support/my_tickets.html', name="Sheldon")

@app.route('/user_tickets', methods=['GET'])
def userTickets():
    return render_template('customer_support/ticket_discussion.html', name="Sheldon")

@app.route('/user_tickets/comments/<int:ticket_ID>', methods=['GET'])
def ticketComments(ticket_ID):
    return render_template('customer_support/ticket_comments.html', name="Sheldon", ticket_ID=ticket_ID)

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
    return render_template('/Report_generation/Individual_report.html', leaderboard=leaderboard_data, name="Sheldon", current_month = month, data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, pie_data = [5,6,7,8], neighbours_helped = '69', number_of_activities = '69')

@app.route('/Report_generation/Community_report')
def Community_report():
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
    return render_template('/Report_generation/Community_report.html', leaderboard=leaderboard_data, name="Sheldon", current_month = month, data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, pie_data = [5,6,7,8], most_contribute = 'Nameless', number_of_activities = '69')

@app.route('/Report_generation/Transactions_report')
def Transactions_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan", "Feb", "March", "April", "May", "June"]
    return render_template('/Report_generation/Transactions_report.html', name="Sheldon",current_month = month, data1 = [5,6,7,8,9,10], data2 = [5,6,7,8,9,10], data3 = [5,6,7,8,9,10],current_year=current_year,listMonths = ListMonths)

@app.route('/Report_generation/saved_reports')
def Saved_report():
    events = [
        {
            "name": "Event 1",
            "report_link": "http://example.com/report/event1"
        },
        {
            "name": "Event 2",
            "report_link": "http://example.com/report/event2"
        },
        {
            "name": "Event 3",
            "report_link": "http://example.com/report/event3"
        }
    ]
    return render_template('/Report_generation/saved_reports.html', name="Sheldon", events = events)


@app.route('/Report_generation/event_list')
def Event_list():
    events = [
        {
            "name": "Event 1",
            "report_link": "http://example.com/report/event1"
        },
        {
            "name": "Event 2",
            "report_link": "http://example.com/report/event2"
        },
        {
            "name": "Event 3",
            "report_link": "http://example.com/report/event3"
        }
    ]
    return render_template('/Report_generation/event_list.html', name="Sheldon", events = events)


@app.route('/Report_generation/Event_details.html')
def Event_details():
    details = {
        'event_name': 'Sample Event',
        'event_date': '2023-07-30',
        'event_description': 'This is a sample event description.',
        'venue': 'Sample Venue',
        'time': '12:00 PM',
        'overall_in_charge': 'John Doe',
        'dateposted': '2023-07-23',
    }


    return render_template('/Report_generation/Event_details.html', name="Sheldon",details = details)

@app.route('/Report_generation/update.html', methods = ['GET', 'POST'])
def update():
    event_details = {
        'event_name': 'Sample Event',
        'event_date': '2023-07-30',
        'event_location': 'Sample City',
        'event_description': 'This is a sample event description.',
        'venue': 'Sample Venue',
        'time': '12:00 PM',
        'overall_in_charge': 'John Doe',
        'dateposted': '2023-07-23',
    }
    update_user_form = CreateUserForm(request.form)
    # if request.method == 'POST' and update_user_form.validate():

        # firebase portion
        # users_dict = {}
        # db = shelve.open('storage.db', 'w')
        # users_dict = db['Users']


        # class portion
        # user = users_dict.get(id)
        # user.set_first_name(update_user_form.first_name.data)
        # user.set_last_name(update_user_form.last_name.data)
        # user.set_gender(update_user_form.gender.data)
        # user.set_membership(update_user_form.membership.data)
        # user.set_remarks(update_user_form.remarks.data)

        # db['Users'] = users_dict
        # db.close()

        # return redirect(url_for('retrieve_users'))
    # else:
    #     users_dict = {}
    #     db = shelve.open('storage.db', 'r')
    #     users_dict = db['Users']
    #     db.close()
    #
    #     user = users_dict.get(id)
    #     update_user_form.first_name.data = user.get_first_name()
    #     update_user_form.last_name.data = user.get_last_name()
    #     update_user_form.gender.data = user.get_gender()
    #     update_user_form.membership.data = user.get_membership()
    #     update_user_form.remarks.data = user.get_remarks()
    #
    #     return render_template('updateUser.html', form=update_user_form)
    return render_template('/Report_generation/update.html', name="Sheldon", form=update_user_form,event=event_details)

#Transaction handling routes
@app.route('/transaction_handling/marketplace')
def marketplace():
    products = [
        {
            'title': 'Fantastic Book',
            'description': 'This is a fantastic book that...',
            'price': 14.99,
            'seller': 'Jane Doe',
            'rating': 4.7,
            'condition': 'Like New',
            'image': 'book.jpg',
        },
        # Add more product dictionaries here for other products
    ]
    return render_template('/transaction_handling/marketplace.html', name="Sheldon", products=products)

if __name__ == '__main__':
    app.run(debug=True, port=5000)