from flask import Flask, render_template, request
from datetime import datetime
from simplex import *
import json

app = Flask(__name__)


@app.context_processor
def inject_now():
    """ Get the time """

    return {'now': datetime.utcnow()}


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home page """

    if request.method == 'POST':
        content = request.get_json()

        quantity_variables = int(content['quantity_variables'])
        quantity_constrains = int(content['quantity_constrains'])
        values = [float(values) for values in content['col_values']]
        z_equation = [(0 - values) for values in content['z_equation']]

        final_result = principal(quantity_variables, quantity_constrains, values, z_equation)

        return json.dumps({'status': 200, 'msg': 'Todo bien', 'data': final_result})

    return render_template('home.html')


@app.route('/results')
def results():
    """ Results page """

    return "Results page"


if __name__ == '__main__':
    app.run(debug=True)
