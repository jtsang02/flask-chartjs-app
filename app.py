from flask import Flask, jsonify, render_template
from readDatabase import prices_open, dates, prices_close, prices_high, prices_low

app = Flask(__name__)

@app.route('/')
def line():
    labels = dates
    values = prices_open
    return render_template("graph.html", labels=labels, values=values)

@app.route('/open')
def openPrices():
    return jsonify({'xValues' : dates, 'yValues' : prices_open})

@app.route('/close')
def closedPrices():
    return jsonify({'xValues' : dates, 'yValues' : prices_close})

@app.route('/high')
def highPrices():
    return jsonify({'xValues' : dates, 'yValues' : prices_high})

@app.route('/low')
def lowPrices():
    return jsonify({'xValues' : dates, 'yValues' : prices_low})

if __name__ == "__main__":
    app.run()