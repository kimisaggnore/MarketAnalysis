import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import urllib.request , socket
from BasicHelperFunctions import *
import numpy as np
import pandas as pd
from datetime import datetime
#from AsynchronousHelperFunctions import *

async def main():
    loop = asyncio.get_event_loop()

    all_companies = construct_symbols()
    proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
    proxy_list = open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n")

    start_time = time.time()
    new_proxy_list = []
    working_proxies = await check_proxies(proxy_list)
    print("--- verifying proxies: %s seconds elapsed ---" % ((time.time() - start_time)))
    
    for i in range(0,10):
        index = 0
        for proxies in working_proxies:
            if proxies != 0:
                new_proxy_list.append(proxy_list[index])
            index += 1
        
        proxies_head = convert_list_to_linked_list(new_proxy_list)
        start_time = time.time()
        indexes = [1]*100
        all_prices = await retrieve_SP_500_prices(indexes, proxies_head, all_companies)
        all_prices = [float(i.replace(',','')) for i in all_prices]
        current_prices = all_prices.copy()
        percent_success, remaining_list = check_num_successful(all_prices)
        print("--- threshold percent: 0.95 ---")
        print("--- remaining prices retrieval: {:.2f} seconds elapsed, {:.2f} percent complete ---".format(time.time() - start_time , percent_success))
        while not percent_success >= .95:
            all_prices = await retrieve_SP_500_prices(remaining_list, proxies_head, all_companies)
            all_prices = [float(i.replace(',','')) for i in all_prices]
            current_prices = merge_prices_lists(current_prices, all_prices, remaining_list)
            percent_success, remaining_list = check_num_successful(current_prices)
            print("--- remaining prices retrieval: {:.2f} seconds elapsed, {:.2f} percent complete ---".format(time.time() - start_time , percent_success))

        print("\n")
        print(current_prices)

        current_prices = np.asarray(current_prices)
        saved_full_times = []
        saved_daily_times = []
        saved_data = []
        saved_data.append(current_prices)
        saved_full_times.append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        saved_daily_times.append(float(datetime.now().strftime("%H"))*60 + float(datetime.now().strftime("%M")) + float(datetime.now().strftime("%S"))/60)
        np.savetxt('Proxy_Cycling/trading_data.csv', saved_data, fmt = "%f", delimiter= ",")
        np.savetxt('Proxy_Cycling/trading_full_time_data.csv', saved_full_times, fmt = "%s", delimiter= ",")
        np.savetxt('Proxy_Cycling/trading_daily_time_data.csv', saved_daily_times, fmt = "%f", delimiter= ",")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

    






