import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
    m=len(stock_price)
    # when there are m data points in stock_price, there are m-n+1 data points in moving_average. For the days before day n, I just ignored them here as they don't affect the strategy. The same holds for oscillator.
    # no need to worry about the NAN here, because as long as the moving average price is NAN, 
    #all the values afterhand are also NAN.
    ma=np.zeros(m-n+1)
    for i in range(m-n+1):
        if len(weights) == 0: # non-weighted average
            ma[i]=np.mean(stock_price[i:i+n])
        else:
            ma[i]=weights@stock_price[i:i+n] # the inner product of weights and stock_price
    return ma


def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.
    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.
    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    m=len(stock_price)
    osc=[]
    if osc_type=='stochastic':
        for i in range(m-n+1):
            highest_price=np.max(stock_price[i:i+n])
            lowest_price=np.min(stock_price[i:i+n])
            delta=stock_price[i+n-1]-lowest_price
            delta_max=highest_price-lowest_price
            osc.append(delta/delta_max)
        
    elif osc_type=='RSI':
        for i in range(m-n+1):
            diff=np.diff(stock_price[i:i+n])
            diff_pos=diff[diff>0]
            diff_neg=diff[diff<0]
            avg_pos=np.mean(diff_pos)
            avg_neg=np.absolute(np.mean(diff_neg))
            # when avg_neg is 0, we cannot compute RSI directly.
            if avg_neg==0:
                RSI=1
            else:
                RS=avg_pos/avg_neg
                RSI=1-1/(1+RS)
            osc.append(RSI)   
    osc=np.array(osc) # osc should be a 1darray
    return osc
