from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.context_processor
def inject_now():
    """ Get the time """

    return {'now': datetime.utcnow()}


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home page """

    if request.method == 'POST':
        print('POST', request.form)
    return render_template('home.html')


@app.route('/results')
def results():
    """ Results page """

    return "Results page"


if __name__ == '__main__':
    app.run(debug=True)
