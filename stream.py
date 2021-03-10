import socketio
from csv import writer
import matplotlib.pyplot as plt

from functools import reduce   # Only in Python 3, omit this in Python 2.x
from decimal import *

# standard Python
sio = socketio.Client()

def append_list_as_row(file,list_of_elem):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

class Currency():
    def __init__(self, name):
        self.name = name
        self.price_data = []
        self.ao = []
        self.buy_ps = []
        self.sell_ps = []
        self.buy_period = []
        self.profit = []
        self.buy_pos = []
        self.sell_pos = []
        self.portfolio = 0
        self.buy_p_ind = []
        self.sell_p_ind = []
        self.count = 0
        self.inds = []

    def check_AO(self):
        if len(self.price_data) >= 34 :
            self.calculate_AO()
            if len(self.buy_period) > 0:
                self.buy_period.append(self.price_data[-1])
            if len(self.buy_ps) == len(self.sell_ps):
                self.check_swing()
            else:
                self.look_to_sell()

    def look_to_sell(self):
        if (self.buy_period[-1] *.99) >= self.buy_period[0]:
            self.sell()
            print('selllllll')

        if len(self.buy_period) > 10:
            if self.ao[-1] < 0:
                self.sell()
                print('selllllll')
                print('buyp, sellp, ao', self.buy_ps[-1], self.sell_ps[-1], self.ao[-1])
        
        
        """
        if len(self.buy_period) >= 5:
            for i in reversed(self.buy_period[-5:]):
                if self.buy_period[i] > self.buy_period[i-1]:
                    break
                if self.buy_period[i] == self.buy_period[-5]:
                    self.sell()
                    print('selllllll')
                    print('buyp, sellp', self.buy_ps[-1], self.sell_ps[-1])
        """

                    
    def sell(self):
        self.sell_ps.append(self.price_data[-1])
        self.profit.append((self.sell_ps[-1] * 100000) - (self.buy_ps[-1] * 100000))
        self.portfolio += self.profit[-1]
        self.sell_p_ind.append(len(self.price_data))
        print('pos', [self.buy_ps[-1], self.sell_ps[-1]])
        print('profit', self.profit[-1])
        print('period', len(self.buy_period))
        self.buy_period = []
        append_list_as_row('buys.csv',['profit:',self.profit[-1], 'portfolio:', self.portfolio,'buy:', self.buy_ps[-1], 'sell:', self.sell_ps[-1],'ao', self.ao[-1] ])



    def check_swing(self):
        if len(self.ao) >= 2:
            print('check swing', self.price_data[-1], "   ", self.ao[-1])
            if self.ao[-1] > 0 and self.ao[-2] < 0:
                self.buy()

    def buy(self):
        self.buy_ps.append(self.price_data[-1])
        self.buy_period.append(self.price_data[-1])
        self.buy_pos.append(self.buy_ps[-1] * 100000)
        self.buy_p_ind.append(len(self.price_data))
        print('buuuuuuyyyy')
        print('buy p', self.buy_ps[-1])

    def sma(self, arr, period):
        sums = 0
        for i in arr:
            sums += i
        return sums / period

    def calculate_AO(self):
        sma_5 = self.sma(self.price_data[-5:], 5)
        sma_34 = self.sma(self.price_data[-34:], 34)
        append_list_as_row('smas.csv', [sma_5, sma_34])
        #print(34,sma_34)
        #print(5,sma_5)
        self.ao.append(sma_5 - sma_34)
        append_list_as_row('ao.csv', [sma_5-sma_34])
        #print('ao', self.ao[-1])

    def show_data(self):
        plt.plot(self.inds, self.price_data)
        plt.show()

gbpusd = Currency('AUDUSD')

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('login', {'userKey': 'siop_YpHaOmAgvLXqju_Q'})

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def message(data):
    print('I received a message!')

@sio.on('handshake')
def on_message(data):
    print('HandShake', data)
    sio.emit('symbolSub', {'symbol': 'USDJPY'})
    sio.emit('symbolSub', {'symbol': 'GBPUSD'})
    sio.emit('symbolSub', {'symbol': 'EURUSD'})


def convert_price(p):
    dec = p.split('.')[1]
    length = len(dec)
    exp = 10**length
    res = int(dec)/exp
    res += int(p.split('.')[0])
    return res


@sio.on('price')
def on_message(data):
    #print('Price Data ', data)
    if data.split(' ')[0] == 'GBPUSD':
        p = data.split(' ')[3]
        price = convert_price(p)
        gbpusd.price_data.append(price)
        append_list_as_row('prices.csv', [price])
        gbpusd.inds.append(gbpusd.count)
        gbpusd.count += 1
        gbpusd.check_AO()
        #gbpusd.show_data()
    


sio.connect('https://marketdata.tradermade.com')