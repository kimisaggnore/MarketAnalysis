import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import urllib.request , socket
from BasicHelperFunctions import *
from AsynchronousHelperFunctions import *

async def main():
    loop = asyncio.get_event_loop()

    all_companies = construct_symbols()
    proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
    proxy_list = open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n")

    start_time = time.time()
    new_proxy_list = []
    working_proxies = await check_proxies(proxy_list)
    
    index = 0
    for proxies in working_proxies:
        if proxies != 0:
            new_proxy_list.append(proxy_list[index])
        index += 1
    print("--- %s seconds ---" % (time.time() - start_time))

    proxies_head = convert_list_to_linked_list(new_proxy_list)
    start_time = time.time()
    indexes = [1]*120
    all_prices = await retrieve_SP_500_prices(indexes, proxies_head, all_companies)
    print(all_prices)
    print("--- %s seconds ---" % (time.time() - start_time))

    current_prices = all_prices.copy()
    percent_success, remaining_list = check_num_successful(all_prices)
    #while not percent_success >= .9:

    all_prices = await retrieve_SP_500_prices(remaining_list, proxies_head, all_companies)
    #percent_success, remaining_list = check_num_successful(all_prices)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(current_prices)
    print("\n")
    print(all_prices)
    
    current_prices, remaining_list = merge_prices_lists(current_prices, all_prices, remaining_list)

    print("\n")
    print(current_prices)
    print("\n")
    print(remaining_list)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
# index = 0
# for proxies in working_proxies:
#     if proxies != 0:
#         new_proxy_list.append(proxy_list[index])
#     index += 1
# print("--- %s seconds ---" % (time.time() - start_time))

# proxies_head = convert_list_to_linked_list(new_proxy_list)
# start_time = time.time()
# indexes = [1]*120
# asyncio.run(retrieve_SP_500_prices(indexes))
# print(all_prices)
# print("--- %s seconds ---" % (time.time() - start_time))

# current_prices = all_prices.copy()
# percent_success, remaining_list = check_num_successful(all_prices)
# #while not percent_success >= .9:

# asyncio.run(retrieve_SP_500_prices(remaining_list))
# #percent_success, remaining_list = check_num_successful(all_prices)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(current_prices)
# print("\n")
# print(all_prices)

# #current_prices, remaining_list = merge_prices_lists(current_prices, all_prices, remaining_list)
    





# while not num_success > .9:
#     proxies_head = convert_list_to_linked_list(new_proxy_list)
#     start_time = time.time()
#     asyncio.run(retrieve_SP_500_prices())
#     print(all_prices)
#     print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
# proxies_head = convert_list_to_linked_list(new_proxy_list)
# asyncio.run(retrieve_SP_500_prices())
# print(all_prices)
# print("--- %s seconds ---" % (time.time() - start_time))

#return prices_list

#retrieve_all_prices()
