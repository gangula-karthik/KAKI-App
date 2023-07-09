from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def marketplace():
    products = [
        {'name': 'Product 1', 'price': 10},
        {'name': 'Product 2', 'price': 20},
        {'name': 'Product 3', 'price': 30}
    ]
    return render_template('marketplace.html', products=products)

if __name__ == '__main__':
    app.run()