from flask import Flask, render_template, request
from datetime import datetime
from SimplexClass import Simplex
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
        print('POST', request.form)
        qv = request.args.get('quantity_variables')
        qc = request.args.get('quantity_constrains')
        cv = request.args.get('col_values')
        zeq = request.args.get('z_equation')
        obj = Simplex(qv, qc, cv, zeq)
        obj.display()
        print(obj.calculate())
        return json.dumps({'status': 200, 'msg': 'Todo bien'})

    return render_template('home.html')


@app.route('/results')
def results():
    """ Results page """

    return "Results page"


if __name__ == '__main__':
    app.run(debug=True)
