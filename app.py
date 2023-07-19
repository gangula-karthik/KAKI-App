import logging
from flask import Flask, request, render_template
import colorlog
from colorama import Fore

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

# Add the handler to Flask's logger
app.logger.addHandler(handler)

# Configure Werkzeug logger
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)
werkzeug_logger.propagate = False

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

class CustomRequestLoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        app.logger.info('Request type: %s', environ.get('REQUEST_METHOD'))
        app.logger.info('Path: %s', environ.get('PATH_INFO'))
        return self._app(environ, start_response)

app.wsgi_app = CustomRequestLoggingMiddleware(app.wsgi_app)

@app.route('/', methods=['GET'])
def index():
    return render_template('template.html', name="Sheldon")
# Change the index.html to template.html to check your work as the index.html is not yet linked

@app.route('/home', methods=['GET'])
def home():
    return render_template('homefeed.html', name="Sheldon")

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
    return render_template('/Report_generation/Individual_report.html', name="Sheldon", current_month = month, data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, pie_data = [5,6,7,8], neighbours_helped = '69', number_of_activities = '69')

@app.route('/Report_generation/Community_report')
def Community_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan","Feb","March","April","May","June"]
    return render_template('/Report_generation/Community_report.html', name="Sheldon", current_month = month, data = [5,6,7,8,9,10], current_year=current_year,listMonths = ListMonths, pie_data = [5,6,7,8], most_contribute = 'Nameless', number_of_activities = '69')

@app.route('/Report_generation/Transactions_report')
def Transactions_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    current_year = now.year
    ListMonths = ["Jan", "Feb", "March", "April", "May", "June"]
    return render_template('/Report_generation/Transactions_report.html', name="Sheldon",current_month = month, data1 = [5,6,7,8,9,10], data2 = [5,6,7,8,9,10], data3 = [5,6,7,8,9,10],current_year=current_year,listMonths = ListMonths)

@app.route('/Report_generation/Saved_report')
def Saved_report():
    return render_template('/Report_generation/Saved_report.html', name="Sheldon")

#Transaction handling routes
@app.route('/transaction_handling/marketplace')
def marketplace():
    return render_template('/transaction_handling/marketplace.html', name="Sheldon")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=5000)