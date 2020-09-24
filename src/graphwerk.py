import os
from numpy import genfromtxt
import matplotlib.pyplot as plt
import mpl_finance
import numpy as np
import uuid
import datetime

# Input your csv file here with historical data

ad = genfromtxt('../financial_data/BINANCE_BTCUSDT_30S_3.csv',
                delimiter=',', dtype=str)
# pd = np.flipud(ad)
pd = ad

buy_dir = '../data/group3/buy/'
sell_dir = '../data/group3/sell/'
try:
    os.mkdir(buy_dir)
    os.mkdir(sell_dir)
except:
    print()


def convolve_sma(array, period):
    return np.convolve(array, np.ones((period,))/period, mode='valid')


def graphwerk(start, finish):
    open = []
    high = []
    low = []
    close = []
    volume = []
    date = []
    for x in range(finish-start):

        # Below filtering is valid for eurusd.csv file. Other financial data files have different orders so you need to find out
        # what means open, high and close in their respective order.
        open.append(float(pd[start][1]))
        high.append(float(pd[start][2]))
        low.append(float(pd[start][3]))
        close.append(float(pd[start][4]))
        volume.append(float(pd[start][5]))
        # date.append(pd[start][0])
        date.append(datetime.datetime.fromtimestamp(
            int(pd[start][0])).isoformat())
        start = start + 1

    close_next = float(pd[finish][4])

    sma = convolve_sma(close, 5)
    smb = list(sma)
    diff = sma[-1] - sma[-2]

    for x in range(len(close)-len(smb)):
        smb.append(smb[-1]+diff)

    fig = plt.figure(num=1, figsize=(3, 3), dpi=50,
                     facecolor='w', edgecolor='k')
    dx = fig.add_subplot(111)
    # mpl_finance.volume_overlay(ax, open, close, volume, width=0.4, colorup='b', colordown='b', alpha=1)
    mpl_finance.candlestick2_ochl(
        dx, open, close, high, low, width=1.0, colorup='g', colordown='r', alpha=0.5)

    plt.autoscale()
    plt.plot(smb, color="blue", linewidth=10, alpha=0.5)
    plt.axis('off')
    comp_ratio = close_next / close[-1]
    print(comp_ratio)

    if close[-1] > close_next:
        print('close value is bigger')
        print('last value: ' + str(close[-1]))
        print('next value: ' + str(close_next))
        print('sell')
        plt.savefig(sell_dir + str(uuid.uuid4()) + '.jpg', bbox_inches='tight')
    else:
        print('close value is smaller')
        print('last value: ' + str(close[-1]))
        print('next value: ' + str(close_next))
        print('buy')
        plt.savefig(buy_dir + str(uuid.uuid4())+'.jpg', bbox_inches='tight')

    # plt.show()
    open.clear()
    close.clear()
    volume.clear()
    high.clear()
    low.clear()
    plt.cla()
    plt.clf()


iter_count = int(len(pd)/4)
print(iter_count)
iter = 0


for x in range(len(pd)-4):
    graphwerk(iter, iter+12)
    iter = iter + 2
