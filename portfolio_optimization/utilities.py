BUCKET_A = [2, 5, 8, 11]
BUCKET_B = [3, 6, 9, 0]
BUCKET_C = [4, 7, 10, 1]
MONTHLY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
investing_months = 60


def print_DRIP_function(stock_sticker, data, dividend_frequency):
    print(
    f" {stock_sticker} | final shares: " + 
    str(data[0]) + " ,remaining cash: "+ str(data[1]) + f" ,final {dividend_frequency} dividend: " + str(data[2]) )

def print_dict(d):
    for key, value in d.items():
        print(f"{key}: {value}")

def calculate_monthly_costs(central_stocks, months):
    """
    Calculate the monthly costs for each stock in the central_stocks list.
    """
    monthly_costs = {
    "janvier": 0,
    "fevrier": 0,
    "mars": 0,
    "avril": 0,
    "mai": 0,
    "juin": 0,
    "juillet": 0,
    "aout": 0,
    "septembre": 0,
    "octobre": 0,
    "novembre": 0,
    "decembre": 0
    }
    
    for stock in central_stocks:
        
        for i in range(12):
            monthly_costs[months[i]] += stock[2][1]*stock[2][3]  # Add the final dividend to the corresponding month


    total_cost = sum(monthly_costs.values())
    
    return monthly_costs, total_cost

def calculate_monthly_dividends(central_stocks, months):
    monthly_dividends = {
    "janvier": 0,
    "fevrier": 0,
    "mars": 0,
    "avril": 0,
    "mai": 0,
    "juin": 0,
    "juillet": 0,
    "aout": 0,
    "septembre": 0,
    "octobre": 0,
    "novembre": 0,
    "decembre": 0
    }

    for stock in central_stocks:
        
        
        if stock[3] == MONTHLY:
            
            for i in range(12):
                monthly_dividends[months[i]] += stock[2][0]*stock[1][0]  
        else :
            for i in stock[3]:
                monthly_dividends[months[i]] += stock[1][2]
    
    return monthly_dividends


def calculate_total_portfolio_value(stocks):
    total_value = 0
    for stock in stocks:
        total_value += stock[1][0] * stock[1][1]  # shares * price
    return total_value


'''
def print_monthly_budget(list,budget):
    for i in range(len(list)):
        budget -= central_stocks[i][2][1] * list[i]
    print("budget: ", budget)

def print_monthly_costs(list):
    cost=0
    for i in range(len(list)):
        cost += central_stocks[i][2][1] * list[i]
    print( cost)
    
'''


def actual_calculate_monthly_dividends(central_stocks,actual_stocks, months):
    monthly_dividends = {
    "janvier": 0,
    "fevrier": 0,
    "mars": 0,
    "avril": 0,
    "mai": 0,
    "juin": 0,
    "juillet": 0,
    "aout": 0,
    "septembre": 0,
    "octobre": 0,
    "novembre": 0,
    "decembre": 0
    }

    for i in range(len(central_stocks)):
        
        if central_stocks[i][3] == MONTHLY:
            
            printable = ""

            for j in range(12):
                monthly_dividends[months[j]] += central_stocks[i][2][0]*actual_stocks[i][1]
        else :

            printable = ""

            for j in central_stocks[i][3]:
                monthly_dividends[months[j]] += central_stocks[i][2][0]*actual_stocks[i][1]
    
    return monthly_dividends