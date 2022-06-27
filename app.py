from flask import Flask, jsonify, render_template
from readDatabase import prices_open, dates_open, prices_close, prices_high, prices_low

app = Flask(__name__)

@app.route('/')
def line():
    labels = dates_open
    values = prices_open
    return render_template("graph.html", labels=labels, values=values)

@app.route('/open')
def openPrices():
    return jsonify({'xValues' : dates_open, 'yValues' : prices_open})

@app.route('/close')
def closedPrices():
    return jsonify({'xValues' : dates_open, 'yValues' : prices_close})

@app.route('/high')
def highPrices():
    return jsonify({'xValues' : dates_open, 'yValues' : prices_high})

@app.route('/low')
def lowPrices():
    return jsonify({'xValues' : dates_open, 'yValues' : prices_low})

if __name__ == "__main__":
    app.run()


# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html
# https://stackoverflow.com/questions/51119495/how-to-setup-environment-variables-for-flask-run-on-windows