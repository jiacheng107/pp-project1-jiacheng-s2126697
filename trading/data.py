import numpy as np
from random import randrange
# URL: https://www.geeksforgeeks.org/randrange-in-python/
def generate_stock_price(days, initial_price, volatility):
    '''
    Generates daily closing share prices for a company,
    for a given number of days.
    inputs: initial_price: a vector that initilizes the initial price for each company
            volatility: a vector i.e.volatility for each company
    output: a days* number of companies matrix
    '''
    n=len(initial_price) #number of companies
    # Set stock_prices to be a zero matrix with #days rows and #companies columns
    stock_prices = np.zeros((days,n))
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0,:] = initial_price
    # Set total_drift to be a zero array with length days
    totalDrift= np.zeros((days,n))
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    # Loop over a range(1, days)
    for day in range(1, days):
        for j in range(n):# loop over stocks to generate a 2darray directly
        # Get the random normal increment
            inc = rng.normal(0,volatility[j],size=1)
        # Add stock_prices[day-1] to inc to get NewPriceToday
            NewPriceToday=stock_prices[day-1,j]+inc
        
        # Make a function for the news
            def news(chance, volatility):
            # Choose whether there's news today
                news_today = rng.choice([0,1],1, p=[1-chance,chance])
            # Randomly choose the duration
                duration=randrange(3,14) #duration randomly ranges from 3 days to 14 days
                if news_today:
                # Calculate m and drift
                    m=rng.normal(0,2)
                    drift = m * volatility
                    final = np.zeros(duration)
                    for i in range(duration):
                        final[i] = drift
                    return final
                else:
                    return np.zeros(duration)
        # Get the drift from the news
            d = news(0.01, volatility[j])
        # Get the duration
            duration = len(d)
        # Add the drift to the next days
            totalDrift[day:day+duration,j] =d[0]# since the elements in d are all the same, I simplepy use the first element
        # Add today's drift to today's price
            NewPriceToday+=totalDrift[day,j]
        # Set stock_prices[day] to NewPriceToday or to NaN if it's negative
            if NewPriceToday <=0:
                stock_prices[day,j] = np.nan
            else:
                stock_prices[day,j] = NewPriceToday
    return stock_prices

def get_data(method='read',initial_price=None,volatility=None):
    '''
    Generate or read a simulated data for one or more stocks over 5 years,
    given their initial prices and volatility
    '''
    if method =='read':
        if initial_price==None and volatility !=None:
            initial_price=input('Please specify the initial price for each stock.')
        elif initial_price!=None and volatility ==None:
            data=np.loadtxt('stock_data_5y.txt')
            sim_data=np.zeros((1825,len(initial_price)))
            for i in range(len(initial_price)):
                sim_data[:,i]=data[1:,0]
                for j in range(20):
                    if abs(data[1][j]-initial_price[i])<abs(sim_data[0][i]-initial_price[i]):
                        sim_data[:,i]=data[1:,j]
                    else:
                        sim_data[:,i]=sim_data[:,i]
        elif initial_price==None and volatility ==None:
            sim_data=data
        else:
            data=np.loadtxt('stock_data_5y.txt')
            sim_data=np.zeros((1825,len(initial_price)))
            for i in range(len(volatility)):
                sim_data[:,i]=data[1:,0]
                for j in range(20):
                    if abs(data[1][j]-initial_price[i])<=abs(sim_data[0][i]-initial_price[i]):
                        sim_data[:,i]=data[1:,j]
                    else:
                        sim_data[:,i]=sim_data[:,i]
            for i in range(len(initial_price)):
                sim_data[:,i]=data[1:,0]
                for j in range(20):
                    if abs(a[1][j]-initial_price[i])<abs(sim_data[0][i]-initial_price[i]):
                        sim_data[:,i]=data[1:,j]
                    else:
                        sim_data[:,i]=sim_data[:,i]                   
    if method=='generate':
        if initial_price==None and volatility !=None:
            initial_price=input('Please specify the initial price for each stock.')
        elif initial_price!=None and volatility ==None:
            volatility=input('Please specify the volatility for each stock.')
        elif initial_price==None and volatility ==None:
            initial_price=input('Please specify the initial price for each stock.')
            volatility=input('Please specify the volatility for each stock.')
        else:
            sim_data=generate_stock_price(1825, initial_price, volatility)                    
    return sim_data
