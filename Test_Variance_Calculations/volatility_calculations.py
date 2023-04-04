import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics 
import statsmodels.api as sm
import time
import math

def update_csv():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    opening_price_list= intel_df["open"].values
    closing_price_list = intel_df["close"].values
    volume_list = intel_df["volume"].values
    percent_changes_list = [round((close_price - open_price)/close_price, 4) for close_price, open_price in zip(closing_price_list, opening_price_list)]
    lognormal_volume_list = [np.log(volume) for volume in volume_list]
    intel_df["lognormal_volume"] = lognormal_volume_list
    intel_df["percent_change"] = percent_changes_list
    intel_df.to_csv(os.path.join(sys.path[0], "Intel_Data.csv"), index = False)

#update_csv()

def plot_percent_changes():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    percent_changes_list = intel_df["percent_change"][-160:]
    std_dev=  statistics.stdev(percent_changes_list)
    mean = statistics.mean(percent_changes_list)
    print(f"mean: {mean}")
    print(f"std_dev: {std_dev}")
    plt.hist(percent_changes_list,200, (-.1, .1))
    sm.qqplot(percent_changes_list, line = 's')
    plt.show() 

def save_percent_changes():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    percent_changes_list = intel_df["percent_change"][-500:]
    percent_changes_list.to_csv("percent_changes.csv", index = False)


def plot_prices():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    closing_price_list = intel_df["close"]
    plt.hist(closing_price_list[3000:],100)
    sm.qqplot(closing_price_list[3000:], line = 's')
    plt.show()
    #plt.hist(closing_price_list,100)

def plot_lognormal_volume():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    lognormal_volume_list = intel_df["lognormal_volume"]
    plt.hist(lognormal_volume_list[3000:],100)
    sm.qqplot(lognormal_volume_list[3000:], line = 's')
    plt.show()

def plot_volume():
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    volume_list = intel_df["volume"]
    plt.hist(volume_list[3000:],100)
    sm.qqplot(volume_list[3000:], line = 's')
    plt.show()

#plot_lognormal_volume()

#Find the subarray of length n with the greatest variance
#How to find whether any added element would increase or decrease the variance -> Is the added element greater or less than one standard deviation? of the mean?
#
def max_volatility_estimator(time_period_start, time_period_end, length):
    start_time = time.time()
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    percent_changes_list = intel_df["percent_change"][slice(time_period_start,time_period_end,1)].tolist()

    cur_sum = sum(percent_changes_list[0:length])
    cur_mean = cur_sum/length
    cur_stddev = statistics.stdev(percent_changes_list[0:length])
    max_stddev = cur_stddev
    at_max = True
    max_start = 0
    max_end = length
    for i in range(1, time_period_end - time_period_start - length):

        cur_end = length + i
        cur_start = i 
    
        cur_sum = cur_sum - percent_changes_list[cur_start] + percent_changes_list[cur_end] 
        cur_mean  = cur_sum/length
        cur_start_val = (percent_changes_list[cur_start-1] - cur_mean)**2
        cur_end_val = (percent_changes_list[cur_end] - cur_mean)**2
        if not at_max:
            if (cur_end_val - cur_start_val > 0):
                if (max_stddev < statistics.stdev(percent_changes_list[cur_start:cur_end])):
                    at_max = True


        if (cur_end_val - cur_start_val > 0 and at_max):
            max_start = cur_start
            max_end = cur_end
            max_stddev = statistics.stdev(percent_changes_list[max_start:max_end])
        else:
            at_max = False


        #print(cur_sum_of_terms)
        #cur_percent_changes_list = percent_changes_list[slice(cur_start, cur_end, 1)]
        # print(cur_start)
        # print(cur_end)
        # print(cur_percent_changes_list)


    end_time = time.time() - start_time
    print(f"end time: {end_time}")
    print(f"maxstart: {max_start}, maxend: {max_end}")
    return max_stddev


def max_volatility_true(time_period_start, time_period_end, length):
    start_time = time.time()
    intel_df = pd.read_csv(os.path.join(sys.path[0], "Intel_Data.csv"))
    percent_changes_list = intel_df["percent_change"][slice(time_period_start,time_period_end,1)].tolist()
    cur_stddev = statistics.stdev(percent_changes_list[0:length])
    max_stddev = cur_stddev
    max_start = 0
    max_end = length
    for i in range(1, time_period_end - time_period_start - length):
        cur_end = length + i
        cur_start = i 
        cur_stddev = statistics.stdev(percent_changes_list[cur_start:cur_end])
        if cur_stddev > max_stddev:
            max_start = cur_start
            max_end = cur_end

        max_stddev = max(cur_stddev, max_stddev)
        

    end_time = time.time() - start_time
    print(f"end time: {end_time}")
    print(f"maxstart: {max_start}, maxend: {max_end}")
    return max_stddev

#print(max_volatility_true(10000, 10600, 20))
#plot_percent_changes()
#save_percent_changes()
plot_prices()