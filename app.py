from flask import Flask, render_template
from database import resultOpen, resultClose, resultHigh, resultLow

app = Flask(__name__)

@app.route('/')
def line():
    
    # print(resultLow)
    xValues = resultLow['Date']
    print(xValues)

    months = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    prices = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]

    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]

    labels = months
    values = prices

    return render_template("graph.html", labels=labels, values=values)

if __name__ == "__main__":
    app.run()


# https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html
# https://stackoverflow.com/questions/51119495/how-to-setup-environment-variables-for-flask-run-on-windows