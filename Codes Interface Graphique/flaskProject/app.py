import time
from flask import Flask, render_template, request, url_for
import sys

sys.path.insert(1, r'D:\Utilisateurs\arnau\Documents\ISIB\MA2\IoT\WebApp')
print(sys.path)
from dbUtil import Database

app = Flask(__name__)
database = Database()


# app.url_for('static', filename='style.css')
# url_for('static', filename='main.js')
# url_for('static', filename='index.html')

@app.route('/')
def index():
    name = "Arnaud"
    return render_template('index.html', name=name)


@app.route('/get_temperature_data')
def send_temperature_data():
    try:
        first = int(request.args.get('first'))
    except:
        first = time.time() - 60000
    all_temperatures = database.get_temperatures()
    data = {}
    for temperature in all_temperatures:
        if temperature["timestamp"] >= first:
            data.update({str(temperature["timestamp"]): temperature["temperature"]})

    return data


if __name__ == '__main__':
    app.run()
