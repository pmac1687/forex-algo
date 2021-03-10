import datetime
from forex_python.converter import get_rate
from csv import writer
import time
import matplotlib.pyplot as plt
import numpy as np

""""t = datetime(2021, 1, 18)  # the 18th of October, 2001
get_rate("USD", "GBP", t)
p = get_rate("GBP", "USD", t)
print(p)"""

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
        self.ind_buys = []
        self.first = False
        self.buy_plots = []
        self.sell_plots = []

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


        if len(self.buy_period) > 5:
            if self.buy_period[0] <= (self.buy_period[-1] * .95):
                self.sell()
                print('selllllll')
                print('buyp, sellp, ao', self.buy_ps[-1], self.sell_ps[-1], self.ao[-1])
                self.first = False
            if self.ao[-1] < 0:
                self.sell()
                print('selllllll')
                print('buyp, sellp, ao', self.buy_ps[-1], self.sell_ps[-1], self.ao[-1])
                self.first = False

        
        
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
        self.sell_plots.append(self.price_data[-1])
        print('pos', [self.buy_ps[-1], self.sell_ps[-1]])
        print('profit', self.profit[-1])
        print('period', len(self.buy_period))
        self.buy_period = []
        append_list_as_row('buys.csv',['index', self.ind_buys[-1],self.count, 'profit:',self.profit[-1], 'portfolio:', self.portfolio,'buy:', self.buy_ps[-1], 'sell:', self.sell_ps[-1],'ao', self.ao[-1] ])



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
        self.buy_plots.append(self.price_data[-1])
        self.ind_buys.append(self.count)
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

        fig, axs = plt.subplots(2)


        #plt.figure(1)
        axs[0].plot(self.inds, self.price_data)
        axs[0].scatter(self.buy_p_ind, self.buy_plots)
        axs[0].scatter(self.sell_p_ind, self.sell_plots)

        #plt.show()
        lst = self.ao[::-1]
        for i in range(33):
            lst.append(0)
        print(len(lst),len(self.inds), lst[::-1])
        #plt.figure(2)
        axs[1].bar(self.inds, lst[::-1])
        plt.show()

def get_data():
    #create date range list
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(725)]
    prices = []
    curr = Currency('GBPUSD')
    for date in date_list:
        #time.sleep(1)
        try:
            price = get_rate("USD", "CAD", date)
            prices.append({'price': price, 'date': date})
            if price not in curr.price_data:
                curr.price_data.append(price)
                append_list_as_row('./csv/gbpusd.csv', [price, date])
                curr.inds.append(curr.count)
                curr.count +=1
                curr.check_AO()
                print(price)

        except:
            print('uhoh', date)
    curr.show_data()
        


if __name__=='__main__':
    get_data()