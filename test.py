from flask import Flask, render_template_string, flash, redirect, url_for, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/flash')
def flash_message():
    flash('Hello, world!')
    return redirect(url_for('index'))

@app.route('/')
def index():
    messages = get_flashed_messages()
    return render_template_string('''
<!doctype html>
<html lang="en">
<head>
    <title>Home</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
</head>
<body>
    {% for message in messages %}
        <div class="toast" id="myToast" data-autohide="false" style="position: absolute; top: 0; right: 0;">
            <div class="toast-header">
                <strong class="mr-auto text-primary">Message</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button>
            </div>
            <div class="toast-body">
                {{ message }}
            </div>
        </div>
    {% endfor %}
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var toastHTMLElement = document.getElementById('myToast');
            if (toastHTMLElement) {
                var toastElement = new bootstrap.Toast(toastHTMLElement);
                toastElement.show();
            }
        });
    </script>
</body>
</html>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
