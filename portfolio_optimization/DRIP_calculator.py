import math
import random
from utilities import *





def DRIP_calculator(
    months: int,
    monthly_dividend: float,
    stock_price: float,
    initial_shares: int = 25,
    extra_shares_per_month: int = 8,
    dividend_frequency: int = 1    ,      # 3 for quarterly dividends, 1 for monthly
    verbose: bool = False
) -> tuple[int, float, float]:
    """
    Simulates DRIP + optional monthly extra share purchases.

    Returns:
      - final share count
      - leftover cash after final month
    """
    shares = initial_shares
    cash = 0.0  # accumulated dividends not yet reinvested

    for month in range(months):
        # 1) collect dividends
        if month % dividend_frequency == 0:
            
            cash += shares * monthly_dividend

        # 2) buy as many whole shares as possible with cash
        new_shares = math.floor(cash / stock_price)
        cash -= new_shares * stock_price

        # 3) optional extra shares (e.g. direct monthly purchase)
        new_shares += extra_shares_per_month

        # 4) update share count
        shares += new_shares
        
        if verbose:
            print(f"Month {month+1}: Shares: {shares}, Cash: {cash:.2f}")

    final_monthly_dividend = shares * monthly_dividend
        
    return shares, cash, final_monthly_dividend




def random_indices(
    n: int,
    subtract: bool = False,
    alpha: float = 1.0,
    max_subset_size: int | None = None,
    no_touch_array: list[int] | None = None
) -> list[int]:
    """
    Returns a random sorted subset of indices from 0 to n-1, excluding any in no_touch_array.
    The subset size is chosen randomly between 1 and available_count, and capped by max_subset_size if provided.

    If subtract is False, selection is uniform.
    If subtract is True, selection is biased by price^alpha, using Efraimidis–Spirakis.

    :param n: total number of items (indices 0 to n-1)
    :param subtract: if True, use price-biased sampling
    :param alpha: exponent for weight bias (alpha>1 accentuates bias toward expensive)
    :param max_subset_size: optional cap on the subset size
    :param no_touch_array: list of indices to exclude from selection
    :return: sorted list of selected indices
    """
    # prepare exclusion set
    exclude = set(no_touch_array) if no_touch_array else set()

    # build available indices
    available = [i for i in range(n) if i not in exclude]
    avail_count = len(available)
    if avail_count == 0:
        return []  # nothing to sample

    # determine subset size k, capped by max_subset_size
    upper = avail_count if max_subset_size is None else min(avail_count, max_subset_size)
    k = random.randint(1, upper)

    if not subtract:
        # uniform random sample from available
        subset = random.sample(available, k)
        return sorted(subset)

    # price-biased sampling without replacement over available
    eps = 1e-12
    keyed = []
    for i in available:
        # extract price weight; adjust as needed to your data structure
        price = central_cost_vector[i][1]  # assume tuple (id, price)
        w = price + eps
        u = random.random()
        # weight to the alpha power accentuates bias
        key = -math.log(u + eps) / (w ** alpha)
        keyed.append((key, i))

    # select k indices with smallest keys
    selected = sorted(keyed, key=lambda x: x[0])[:k]
    subset = [idx for _, idx in selected]
    return sorted(subset)

def apply_uniform(base_array: list[int], indices_to_modify: list[int], subtract: bool = False) -> list[int]:
    
    
    result = base_array.copy()
    for idx in indices_to_modify:
        if subtract:
            result[idx] -= 1
        else:
            result[idx] += 1
    return result


def profit_function(assets,budget):
    profit = 0

    if estimate_cost(assets, budget) < 0:
        return -1
    
    elif assets == [1]+ [0]*(len(assets)-1):
        return -1
    
    for i in range(len(assets)):
        profit += assets[i] * ((central_cost_vector[i][0] * 12)/ central_cost_vector[i][1])

    return profit


def estimate_cost(affectation,budget,substract=False,verbose=False):

    al = budget
    

    #if verbose: 
        #print("affectation: ", affectation)
        #print("budget: ", budget)

    for i in range(len(affectation)):
        if substract:
            al += central_cost_vector[i][1]*affectation[i]
        else:
            al -= central_cost_vector[i][1]*affectation[i]
        

    return al

def verificator(beam):
    mask = []
    for asset,budget in beam:
        if budget > 0.84:
            mask.append(1)
        else:
            mask.append(0)

    if sum(mask) > 0:
        return True
    return False


def infiltrator(beam, newanew_a):

    imperial_costs = [profit_function(ship[0], imperial_cost) for ship in beam]
    #print('imperium', imperial_costs)

    index = imperial_costs.index(min(imperial_costs))
    beam[index][0] = newanew_a[0]
    beam[index][1] = estimate_cost(newanew_a[0], imperial_cost,verbose=True)
    

        
def noyau_magitech(assets, budget,central_cost_vector, randomness, beam_length):


    initial_assets = assets
    tracker = 0
    
    budget = estimate_cost(assets, budget)

    best_n_affectation = [0]*len(initial_assets)

    beam = [[initial_assets,budget]]                           # max =      
    nnn = 0
    
    while verificator(beam) > 0.84:
        #print(beam)
        #print(verificator(beam))
        #print('iteration: ', nnn, '____________________________________')
        #print('first budget: ', budget)

        best_n_affectation = [0]*len(initial_assets)
        affectation_found = False

        for empire_ship in beam:

            if empire_ship[1] > 0.84:
                for _ in range(1000):

                    distribution = random_indices(len(empire_ship[0]))

                    #print('distribution: ', distribution)
        
                    distribution_cost_vector = [1 if i in distribution else 0 for i in range(len(central_cost_vector))]
                    best_cost_vector  =  [1 if i in best_n_affectation else 0 for i in range(len(central_cost_vector))]

                    #print(profit_function(distribution_cost_vector, budget), ' >? ', profit_function(best_cost_vector, budget))

                    if (profit_function(distribution_cost_vector,empire_ship[1])) > profit_function(best_cost_vector, empire_ship[1]):
                        best_n_affectation = distribution

                        '''if len(beam) < beam_length:
                            beam.append(new_affectation)'''
                        affectation_found = True

                if tracker %3 == 2:

                    distribution = random_indices(len(empire_ship[0]), subtract=True, alpha=2, max_subset_size=4, no_touch_array=[i for i, value in enumerate(empire_ship[0]) if value == 1])                                                      
                    distribution2 = random_indices(len(initial_assets), subtract=True, alpha=3, max_subset_size=3, no_touch_array=[i for i, value in enumerate(initial_assets) if value == 1])
                    distribution3 = random_indices(len(initial_assets), subtract=True, alpha=4, max_subset_size=2, no_touch_array=[i for i, value in enumerate(initial_assets) if value == 1])

                    if len(beam) < beam_length:
                        beam.append([apply_uniform(empire_ship[0], distribution2, subtract=True), estimate_cost([1 if i in distribution2 else 0 for i in range(len(central_cost_vector))], empire_ship[1], substract=True)])

                    else:
                        #print("AAAAAAAAAAAH 2", beam, apply_uniform(empire_ship[0], distribution2, subtract=True))
                        infiltrator(beam, apply_uniform([empire_ship[0],estimate_cost(empire_ship[0],imperial_cost)], distribution2, subtract=True))

 
                    if len(beam) < beam_length:

                        beam.append([apply_uniform(empire_ship[0], distribution3, subtract=True), estimate_cost([1 if i in distribution3 else 0 for i in range(len(central_cost_vector))], empire_ship[1], substract=True)])
                    
                    else:
                        #print("AAAAAAAAAAAH 3", beam, apply_uniform(empire_ship[0], distribution3, subtract=True))
                        infiltrator(beam, apply_uniform([empire_ship[0],estimate_cost(empire_ship[0],imperial_cost)], distribution3, subtract=True))


                    empire_ship[0] = apply_uniform(empire_ship[0], distribution, subtract=True)
                    
                    cost_vector = [1 if i in distribution else 0 for i in range(len(central_cost_vector))]

                    empire_ship[1] = estimate_cost(cost_vector, empire_ship[1], substract=True)
                     
                #print('best_n_affectation: ', best_n_affectation)
                
                if affectation_found:
                    empire_ship[0] = apply_uniform(empire_ship[0], best_n_affectation, subtract=False)

                    cost_vector =[1 if i in best_n_affectation else 0 for i in range(len(central_cost_vector))]
                    
                    empire_ship[1] = estimate_cost(cost_vector, empire_ship[1])

                    #print(budget)

                    nnn+=1
                
                tracker += 1
                
                #print('____________________________________')

            

    

    
    #print("final assets: ", initial_assets)

    print("beam", beam)

    initial_assets = [0]*len(initial_assets)
    return beam



imperial_cost = 583.3333333

central_cost_vector = [[0.06,6.14], [0.09,11.89], [0.0065,0.84], [0.068,12.20], 
                       [0.0583,10.86], [0.03,4.69], [0.0612,10.463], [0.1,20.12],

                       [0.5875,40.68], [0.18,8.03], [0.105,5.72], [0.29,17.15],
                        [0.500735,23.88], [0.32314875,27.66], [0.725,60.92], [0.457737,37.66],
                        [0.2,10.8], [0.5,28.27]
                       
                       
                       ]

algorithm_result = noyau_magitech(18*[1], imperial_cost,central_cost_vector, 0.1, 5)    #[6,5,30,4,10,5,7,4,2]

M_AX_Dux = 18*[0]

for imperial_ship in algorithm_result:
    if profit_function(imperial_ship[0], imperial_cost) > profit_function(M_AX_Dux, imperial_cost):
        M_AX_Dux = imperial_ship[0]


algorithm_result = M_AX_Dux

print("\nalgorithm result \n___________________________________\n", algorithm_result, "\n___________________________________")

# [5, 4, 6, 4, 4, 6, 4, 4]
# [11, 3, 21, 2, 1, 9, 3, 1]
#




#TODO add a system that manages conditions on affections (eg. never buy 10 and ore CJ.TO stocks monthly)


CJ_TO = ("CJ_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.06, stock_price=6.14, initial_shares=33, extra_shares_per_month=algorithm_result[0]      , dividend_frequency=1), [0.06, 6.14, 25, algorithm_result[0]],MONTHLY)
FRU_TO = ("FRU_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.09, stock_price=11.89, initial_shares=15, extra_shares_per_month=algorithm_result[1]  , dividend_frequency=1), [0.09, 11.89, 12, algorithm_result[1]], MONTHLY)
SRR_VN = ("SRR_VN",DRIP_calculator(months=investing_months, monthly_dividend=0.0065, stock_price=0.84, initial_shares=207, extra_shares_per_month=algorithm_result[2] , dividend_frequency=1), [0.0065, 0.84, 160, algorithm_result[2]], MONTHLY)
APLE = ("APLE",DRIP_calculator(months=investing_months, monthly_dividend=0.0952, stock_price=12.20, initial_shares=6, extra_shares_per_month=algorithm_result[3]     , dividend_frequency=1), [0.0952, 12.20, 10, algorithm_result[3]], MONTHLY)
HR_UN_TO = ("HR_UN_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.05, stock_price=10.68, initial_shares=10, extra_shares_per_month=0, dividend_frequency=1), [0.05, 10.68, 10, 0], MONTHLY)

DIR_UN_TO = ("DIR_UN_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.0583  , stock_price=10.86, initial_shares=5, extra_shares_per_month=algorithm_result[4], dividend_frequency=1), [0.0583, 10.86, 10, algorithm_result[4]], MONTHLY)
NWH_UN_TO = ("NWH_UN_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.03  , stock_price=4.69, initial_shares=25, extra_shares_per_month=algorithm_result[5]   , dividend_frequency=1), [0.03, 4.69, 21, algorithm_result[5]], MONTHLY)
SRRTF = ("SRRTF",DRIP_calculator(months=investing_months, monthly_dividend=0.1008, stock_price=10.463, initial_shares=5, extra_shares_per_month=algorithm_result[6]          , dividend_frequency=1), [0.1008, 10.463, 9, algorithm_result[6]], MONTHLY)
NPI_TO = ("NPI_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.1, stock_price=22.49, initial_shares=13, extra_shares_per_month=algorithm_result[7]            , dividend_frequency=1), [0.1, 20.12, 14, algorithm_result[7]], MONTHLY)

CNQ_TO = ("CNQ_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.5875, stock_price=40.68, initial_shares=2, extra_shares_per_month=algorithm_result[8],   dividend_frequency=3), [0.5875, 40.68, 2, 0], BUCKET_B)
KPT_TO = ("KPT_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.18, stock_price=8.03, initial_shares=13, extra_shares_per_month=algorithm_result[9],     dividend_frequency=3), [0.18, 8.03, 12, 0], BUCKET_B)
XTC_TO = ("XTC_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.105 , stock_price=5.72, initial_shares=4, extra_shares_per_month=algorithm_result[10],    dividend_frequency=3), [0.105, 5.72, 17, 0], BUCKET_A)
ADN_TO = ("ADN_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.29 , stock_price=17.15, initial_shares=3, extra_shares_per_month=algorithm_result[11],    dividend_frequency=3) , [0.29, 17.15, 6, 0], BUCKET_B)

PFE = ("PFE",DRIP_calculator(months=investing_months, monthly_dividend=0.500735 , stock_price=23.88, initial_shares=4, extra_shares_per_month=algorithm_result[12],     dividend_frequency=3) , [0.500735, 23.88, 3, 0], BUCKET_A)
AT_T = ("AT_T",DRIP_calculator(months=investing_months, monthly_dividend=0.32314875 , stock_price=27.66, initial_shares=4, extra_shares_per_month=algorithm_result[15],    dividend_frequency=3) , [0.32314875, 27.66, 3, 0], BUCKET_C)
EMA_TO = ("EMA_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.725 , stock_price=60.92, initial_shares=2, extra_shares_per_month=algorithm_result[13],    dividend_frequency=3) , [0.725, 60.92, 2, 0], BUCKET_C)
CU_TO = ("CU_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.4577 , stock_price=37.66, initial_shares=4, extra_shares_per_month=algorithm_result[14],    dividend_frequency=3) , [0.4577, 37.77, 3, 0], BUCKET_A)

ET_TO = ("ET_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.2, stock_price=10.80, initial_shares=2, extra_shares_per_month=algorithm_result[16],    dividend_frequency=3), [0.2, 10.80, 10, 4], BUCKET_A)
LIF_TO = ("LIF_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.5, stock_price=28.27, initial_shares=3, extra_shares_per_month=algorithm_result[17]   , dividend_frequency=3), [0.5, 29.21, 5, 1], BUCKET_C)


'''
#TSLY_TO = ("TSLY_TO",DRIP_calculator(months=investing_months, monthly_dividend=0.27 , stock_price=8.35, initial_shares=18, extra_shares_per_month=algorithm_result[4], dividend_frequency=1), [0.27, 8.35, 160, algorithm_result[4]], MONTHLY)

SPRE  = ("SPRE",DRIP_calculator(months=36, monthly_dividend=0.05695 , stock_price=19.60, initial_shares=5, extra_shares_per_month=2, dividend_frequency=1) , [0.05695, 19.60, 6, 3], MONTHLY)


WJX_TO = (DRIP_calculator(months=investing_months, monthly_dividend=0.35, stock_price=17.49, initial_shares=100, extra_shares_per_month=0, dividend_frequency=3), [0.35, 17.49, 6, 2], BUCKET_A)
VCI_TO = (DRIP_calculator(months=investing_months, monthly_dividend=0.12 , stock_price=6, initial_shares=100, extra_shares_per_month=0, dividend_frequency=3) , [0.12, 6, 16, 7], BUCKET_C)
ARE_TO = (DRIP_calculator(months=investing_months, monthly_dividend=0.19 , stock_price=15.40, initial_shares=100, extra_shares_per_month=0, dividend_frequency=3), [0.19, 15.40, 6, 3], BUCKET_B)
QQQ_TO = (DRIP_calculator(months=investing_months, monthly_dividend=0.32 , stock_price=21.99, initial_shares=100, extra_shares_per_month=0, dividend_frequency=1), [0.32, 21.99, 2, 2], MONTHLY)

'''
# in case of seeing this here, TODO: set up authentificator app questrade

def print_DRIP_stock_values(central_stocks):
    
    for i in central_stocks:
        print_DRIP_function(i[0], i[1], "monthly")
   

#goal_central_stocks = [CJ_TO, FRU_TO, SRR_VN, DIR_UN_TO, NWH_UN_TO, SRRTF, NPI_TO,PFE, AT_T, CU_TO, EMA_TO, CNQ_TO, KPT_TO, XTC_TO, ADN_TO,HR_UN_TO,ET_TO,LIF_TO] #[CJ_TO, CNQ_TO, FRU_TO, SRR_VN, LIF_TO, KPT_TO, ET_TO, WJX_TO, VCI_TO, ADN_TO, XTC_TO, ARE_TO ,T_ETF,QQQ_TO]

central_stocks = [CJ_TO, FRU_TO, SRR_VN,APLE, DIR_UN_TO, NWH_UN_TO, SRRTF, NPI_TO  ,CNQ_TO, KPT_TO, XTC_TO, ADN_TO, PFE, AT_T,  EMA_TO, CU_TO, ET_TO,LIF_TO] #[CJ_TO, CNQ_TO, FRU_TO, SRR_VN, LIF_TO, KPT_TO, ET_TO, WJX_TO, VCI_TO, ADN_TO, XTC_TO, ARE_TO ,T_ETF,QQQ_TO]


months = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]

#actual_stocks = [33,15,205,5,24,5,13,3,3,4,3,3,13,4,3  ]

visible = [
    ["CJ.TO",33],
    ["FRU.TO",15],
    ["SRR.VN",208],
    ["DIR.UN.TO",5],
    ["NWH.UN.TO",26],
    ["SRRTF",5],
    ["NPI.TO",13],
    ["PFE",4],
    ["AT&T",4],
    ["CU.TO",4],
    ["EMA.TO",2],
    ["CNQ.TO",2],
    ["KPT.TO",13],
    ["XTC.TO",4],
    ["ADN.TO",3],
    ["HR_UN_TO",10],
    ["ET.TO",2],
    ["LIF.TO",3]
]

visible_actuel = [
    ["CJ.TO",33],
    ["FRU.TO",15],
    ["SRR.VN",205],
    ["DIR.UN.TO",5],
    ["NWH.UN.TO",24],
    ["SRRTF",5],
    ["NPI.TO",13],
    ["PFE",2],
    ["AT&T",2],
    ["CU.TO",2],
    ["EMA.TO",1],
    ["CNQ.TO",3],
    ["KPT.TO",13],
    ["XTC.TO",4],
    ["ADN.TO",3],
    ["APLE",6]
    
]
# 1 CNQ = 43.11 transformer en 1 CU + 1 NWH.UN, rest = SRR.VN
# sell 1 AAPL for 2 pfizer and 2 At T
# buy 1 EMA ; buy 2 ET.TO ; but one CU
# buy 1 nwh.un ; rest = srr.vn

'''
#current
visible = [
    ["CJ.TO",33],
    ["FRU.TO",15],
    ["SRR.VN",205],
    ["DIR.UN.TO",5],
    ["NWH.UN.TO",24],
    ["SRRTF",5],
    ["NPI.TO",13],
    ["PFE",3],
    ["AT&T",3],
    ["CU.TO",4],
    ["EMA.TO",3],
    ["CNQ.TO",3],
    ["KPT.TO",13],
    ["XTC.TO",4],
    ["ADN.TO",3],
    ["APLE",6]
   
]'''

'''

print("Monthly costs: ")
print_dict(calculate_monthly_costs(central_stocks, months)[0])
'''

'''print("\n")
print("Monthly dividends: ")
print_dict(actual_calculate_monthly_dividends(goal_central_stocks,visible, months)) #visible_actuel
print("\n")'''


           
print_DRIP_stock_values(central_stocks)
print('\n')


print_dict(calculate_monthly_dividends(central_stocks, months))