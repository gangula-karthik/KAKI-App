from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', name="Sheldon")

@app.route('/Report_generation/Individual_report')
def Individual_report():
    return render_template('/Report_generation/Individual_report.html', name="Sheldon")

@app.route('/Report_generation/Community_report')
def Community_report():
    return render_template('/Report_generation/Community_report.html', name="Sheldon")

@app.route('/Report_generation/Transactions_report')
def Transactions_report():
    return render_template('/Report_generation/Transactions_report.html', name="Sheldon")

@app.route('/Report_generation/Saved_report')
def Saved_report():
    return render_template('/Report_generation/Saved_report.html', name="Sheldon")

if __name__ == '__main__':
    app.run(debug=True, port=5000)