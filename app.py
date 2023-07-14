from flask import Flask,  render_template
import datetime



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('template.html', name="Sheldon")
# Change the index.html to template.html to check your work as the index.html is not yet linked

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
    return render_template('/Report_generation/Individual_report.html', name="Sheldon", current_month = month, data = [5,6,7,8,9,10])

@app.route('/Report_generation/Community_report')
def Community_report():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return render_template('/Report_generation/Community_report.html', name="Sheldon", current_month = month, data = [5,6,7,8,9,10])

@app.route('/Report_generation/Transactions_report')
def Transactions_report():
    return render_template('/Report_generation/Transactions_report.html', name="Sheldon")

@app.route('/Report_generation/Saved_report')
def Saved_report():
    return render_template('/Report_generation/Saved_report.html', name="Sheldon")

#Transaction handling routes
@app.route('/transaction_handling/marketplace')
def marketplace():
    return render_template('/transaction_handling/marketplace.html', name="Sheldon")

if __name__ == '__main__':
    app.run(debug=True, port=5000)