from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', name="Sheldon")

if __name__ == '__main__':
    app.run(debug=True, port=5000)