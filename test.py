from functools import reduce   # Only in Python 3, omit this in Python 2.x
from decimal import *
import math
from csv import writer
import requests


# Open file in append mode
with open('audusd-2-18-20--12pm-200mins.csv', 'a+', newline='') as write_obj:
    # Create a writer object from csv module
    csv_writer = writer(write_obj)
    # Add contents of list as last row in the csv file
    count = 13
    for i in range(60):
        if i < 10:
            i = f'0{i}'
        if int(i) < 60:
            minute = f'{count}:{i}'
        else:
            minute = f'{count}:{i%60}'
        r = requests.get(f'https://marketdata.tradermade.com/api/v1/minute_historical?currency=AUDUSD&date_time=2021-02-18-{minute}&api_key=BXd0QzuLUklHBzY7T2L0')
        if i == 59:
            count += 1

        print(r.json())
        res = r.json()
        csv_writer.writerow(['close:', r.json()['close'], 'currency:', r.json()['currency'], 'date:', res['date_time'], 'high:', res['high'], 'low', res['low'], 'open', res['open']])
