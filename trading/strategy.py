# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
import trading.indicators as ind
import math

def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    
    #important: when price of a stock is nan, then sell all the shares of that stock at price 0
    rng = np.random.default_rng()
    num_stock=stock_prices.shape[1]
    days=stock_prices.shape[0]
    
    #create portfolio at day 0
    portfolio=proc.create_portfolio([amount]*num_stock, stock_prices, fees, ledger=ledger)  
    num_transaction=math.floor(days/period) 
    for i in range(1,num_transaction+1):
        # 0: buy 1: do nothing 2:sell
        for j in range(num_stock):
            if np.isnan(stock_prices[i,j])==True: # sell at price 0
                proc.sell(period*i, j, np.zeros((days,num_stock)), fees, portfolio, ledger)
                break
            else:
                action=rng.choice([0,1,2],1, p=[1/3,1/3,1/3]) #determine the action with equal probability
                if action==0: # buy stock j
                    proc.buy(period*i, j, amount, stock_prices, fees, portfolio, ledger)# price is the price on the last day in each period
                elif action==2: #sell stock j 
                    proc.sell(period*i, j, stock_prices, fees, portfolio, ledger)              
    #then, if there are some remaining stocks, we sell them in the last period
    for k in range(num_stock):
        if portfolio[k]!=0:
            proc.sell(days-1, k, stock_prices, fees, portfolio, ledger)  
    return None   

def crossing_averages(stock_prices, n, m, amount=5000, fees=20, ledger='ledger_crossing_average.txt'):
    '''
    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    num_stock=stock_prices.shape[1]
    days=stock_prices.shape[0]
    
    #create portfolio at day 0
    portfolio=proc.create_portfolio([amount]*num_stock, stock_prices, fees, ledger=ledger)   
    #loop for each stock
    for i in range(num_stock):
        #to better compare the values of FMA and SMA, I force the length of them to be the number of days by adding n-1 "0"s in           #the beginning of the FMA and SMA.
        FMA=np.hstack(([0]*(n-1),ind.moving_average(stock_prices[:,i],n,weights=[])))
        SMA=np.hstack(([0]*(m-1),ind.moving_average(stock_prices[:,i],m,weights=[])))
        for j in range(m,days-1):
            if np.isnan(FMA[j])==False:# FMA is not nan, then SMA is not nan (i.e. price is not nan)
                if (FMA[j]-SMA[j])*(FMA[j+1]-SMA[j+1])<0: # a crossing occurs
                    if FMA[j+1]>SMA[j+1]:# FMA crosses SMA from below, buy stock i at day j
                        proc.buy(j, i, amount, stock_prices, fees, portfolio, ledger)
                    elif FMA[j+1]<SMA[j+1]: # FMA crosses SMA from above, sell stock i at day j
                        proc.sell(j, i, stock_prices, fees, portfolio, ledger)
                else:
                    portfolio=portfolio

            else: #sell at price 0
                proc.sell(j, i, np.zeros((days,num_stock)), fees, portfolio, ledger)
                break
    #then, if there are some remaining stocks, we sell them on the last day
    for k in range(num_stock):
        if portfolio[k]!=0:
            proc.sell(days-1, k, stock_prices, fees, portfolio, ledger)           
    return None 

def momentum(stock_prices, threshold_high, threshold_low, amount=5000, fees=20,n=7,m=5,cool_period=7, osc_type='stochastic', ledger='ledger_momentum.txt'):
    '''

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    
    general thought: buy only if it's stayed below the threshold for a number of consecutive m days,
                     sell only if it's stayed above the threshold for a number of consecutive m days.
    '''
    num_stock=stock_prices.shape[1]
    days=stock_prices.shape[0]
    
    #create portfolio at day 0
    portfolio=proc.create_portfolio([amount]*num_stock, stock_prices, fees, ledger=ledger) 
    for i in range(num_stock): 
        # to create a osc array with length of days, we add a array of all elements equal 0.5 to original osc.As 0.5<0.7
        # and 0.5>0.3
        osc=np.hstack(([0.5]*(n-1),ind.oscillator(stock_price=stock_prices[:,i], n=n, osc_type=osc_type)))
        flag=0 # count for cool_down period
        for j in range(days-m+2): # check from day 0 to day days-m+1
            if flag>0:
                flag-=1
                continue
            if np.all(np.isnan(osc[j:j+m])==False)==True: # there is no nan
                # if from day j to day j+m-1, all osc> threshold_high, then sell the stock at day j+m-1
                if np.all(osc[j:j+m]>threshold_high)==True: 
                    proc.sell(j+m-1, i, stock_prices, fees, portfolio, ledger)
                    flag=cool_period
                # if from day j to day j+m-1, all osc< threshold_low, then buy the stock at day j+m-1
                elif np.all(osc[j:j+m]<threshold_low)==True: #buy
                    proc.buy(j+m-1, i, amount, stock_prices, fees, portfolio, ledger)
                    flag=cool_period
                else:
                    portfolio=portfolio
            else: # sell at priice 0
                proc.sell(j,i,np.zeros((days,num_stock)),fees,portfolio,ledger)
                break       
    for k in range(num_stock):
        if portfolio[k]!=0:
            proc.sell(days-1, k, stock_prices, fees, portfolio, ledger)
    return None


