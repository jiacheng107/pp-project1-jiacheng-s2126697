# Evaluate performance.
import trading.data as data
import trading.strategy as strategy

def read_ledger(filename):
    import matplotlib.pyplot as ppl

    class transaction:

        def __init__(self, trans_type, day, stock_no, trading_num, trading_price, trading_amount):
            self.trans_type = trans_type
            self.day = int(day)
            self.stock_no = int(stock_no)
            self.trading_num = float(trading_num)
            self.trading_price = float(trading_price)
            self.trading_amount = float(trading_amount)

        def __eq__(self, other):
            if self.day == other.day:
                return True
            return False

        def __lt__(self, other):
            if self.day < other.day:
                return True
            return False

    num_transactions = 0
    num_money_hold = 0  # i.e., overall profit
    num_money_spent = 0
    num_money_earned = 0
    list_money_hold = list()
    list_money_hold_day_axis = list()
    transactions = list()
    with open(filename, 'r', encoding='UTF-8') as f:
        fls = f.readlines()
        for fl in fls:
            infos = fl.strip().split(',')
            if len(infos) == 0:
                return False
            transactions.append(transaction(infos[0], infos[1], infos[2], infos[3], infos[4], infos[5]))
    num_transactions = len(transactions)
    transactions = sorted(transactions)  # sort transactions by day
    for t in transactions:
        num_money_hold += t.trading_amount 
        num_money_spent += t.trading_amount if t.trans_type == 'buy' else 0
        num_money_earned += t.trading_amount if t.trans_type == 'sell' else 0
        list_money_hold.append(num_money_hold)
        list_money_hold_day_axis.append(t.day)
    print(f"total number of transactions performed: {num_transactions}")
    print(f"total amount spent over the past 5 years: {num_money_spent}")
    print(f"total amount earned over the past 5 years: {num_money_earned}")
    print(f"overall profit or loss over the past 5 years: {num_money_hold}")
    ppl.figure()
    ppl.plot(list_money_hold_day_axis, list_money_hold)
    ppl.title(filename)
    ppl.show()
    
def modify_text(filename): # truncating file
    with open(filename, "r+") as f:
        read_data = f.read()
        f.seek(0)# locate at the first row of the file
        f.truncate() 
        
def read_ledger_2(filename): # define another fuction to only return the total profit
    import matplotlib.pyplot as ppl

    class transaction:

        def __init__(self, trans_type, day, stock_no, trading_num, trading_price, trading_amount):
            self.trans_type = trans_type
            self.day = int(day)
            self.stock_no = int(stock_no)
            self.trading_num = float(trading_num)
            self.trading_price = float(trading_price)
            self.trading_amount = float(trading_amount)

        def __eq__(self, other):
            if self.day == other.day:
                return True
            return False

        def __lt__(self, other):
            if self.day < other.day:
                return True
            return False

    num_transactions = 0
    num_money_hold = 0  # i.e., overall profit
    num_money_spent = 0
    num_money_earned = 0
    list_money_hold = list()
    list_money_hold_day_axis = list()
    transactions = list()
    with open(filename, 'r', encoding='UTF-8') as f:
        fls = f.readlines()
        for fl in fls:
            infos = fl.strip().split(',')
            if len(infos) == 0:
                return False
            transactions.append(transaction(infos[0], infos[1], infos[2], infos[3], infos[4], infos[5]))
    num_transactions = len(transactions)
    transactions = sorted(transactions)  # sort transactions by day
    for t in transactions:
        num_money_hold += t.trading_amount 
        num_money_spent += t.trading_amount if t.trans_type == 'buy' else 0
        num_money_earned += t.trading_amount if t.trans_type == 'sell' else 0
        list_money_hold.append(num_money_hold)
        list_money_hold_day_axis.append(t.day)
        
    return num_money_hold
    
    


