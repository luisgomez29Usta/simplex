from flask import Flask, render_template, request

app = Flask(__name__)


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
