# importing the flask library files
from flask import Flask, Response
import json
from flask_cors import CORS
import csv

#create flask web app object
app = Flask(__name__)
CORS(app)

# define http route
@app.route("/")
def index():

    with open('../prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        arr1 = []
        for row in csv_reader:
            arr1.append({'price': row})
        print(arr1)
    with open('../ao.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        arr2 = []
        for row in csv_reader:
            arr2.append({'ao': row})
        print(arr2)
    with open('../smas.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        arr3 = []
        for row in csv_reader:
            arr3.append({'sma': row})
        print(arr3)
        return json.dumps([arr1,arr2,arr3])

#run the app
if __name__ == "__main__":
    app.run(debug=True)