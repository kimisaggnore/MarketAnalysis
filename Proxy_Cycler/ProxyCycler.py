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
    proxies_head = convert_list_to_linked_list(open(os.path.join(sys.path[0], "proxies.txt"), "r").read().strip().split("\n"))
    proxy_list = open(os.path.join(sys.path[0], "proxies.txt"), "r").read().strip().split("\n")

    start_time = time.time()
    new_proxy_list = []
    working_proxies = await check_proxies(proxy_list)
    print("--- verifying proxies: %s seconds elapsed ---" % ((time.time() - start_time)))
    # saved_full_times = np.loadtxt('Proxy_Cycling/trading_full_time_data.csv', dtype = str)
    # saved_daily_times = np.loadtxt('Proxy_Cycling/trading_daily_time_data.csv', dtype= float)
    # saved_data = np.loadtxt('Proxy_Cycling/trading_data.csv', dtype= str)
    saved_full_times = []
    saved_daily_times = []
    saved_data = []
    for _ in range(0,1):
        index = 0
        for proxies in working_proxies:
            if proxies != 0:
                new_proxy_list.append(proxy_list[index])
            index += 1
        
        proxies_head = convert_list_to_linked_list(new_proxy_list)
        start_time = time.time()
        indexes = [1]*100
        all_prices, all_volumes = await retrieve_SP_500_data(indexes, proxies_head, all_companies)
        all_prices = [float(i.replace(',','')) for i in all_prices]
        all_volumes = [float(i) if i == '-1' else i for i in all_volumes]
        current_prices = all_prices.copy()
        current_volumes = all_volumes.copy()
        percent_success, remaining_list = check_num_successful(all_prices)
        print("--- threshold percent: 0.95 ---")
        print("--- remaining prices retrieval: {:.2f} seconds elapsed, {:.2f} percent complete ---".format(time.time() - start_time , percent_success*100))
        trials = 0
        while not percent_success >= .95 and trials <= 5:
            all_prices, all_volumes = await retrieve_SP_500_data(remaining_list, proxies_head, all_companies)
            all_prices = [float(i.replace(',','')) for i in all_prices]
            all_volumes = [float(i) if i == '-1' else i for i in all_volumes]
            current_prices = merge_lists(current_prices, all_prices)
            current_volumes = merge_lists(current_volumes, all_volumes)
            percent_success, remaining_list = check_num_successful(current_prices)
            trials += 1
            print("--- remaining prices retrieval: {:.2f} seconds elapsed, {:.2f} percent complete ---".format(time.time() - start_time , percent_success*100))

        print("\n")
        print(current_prices)
        print(current_volumes)

        #current_prices = np.asarray(current_prices)
        saved_data.append(current_prices)
        saved_full_times.append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        saved_daily_times.append(float(datetime.now().strftime("%H"))*3600 + float(datetime.now().strftime("%M"))*60 + float(datetime.now().strftime("%S")))
        np.savetxt(os.path.join(sys.path[0], "trading_data.csv"), np.asarray(saved_data), fmt = "%f", delimiter= ",")
        np.savetxt(os.path.join(sys.path[0], "trading_full_time_data.csv"), np.asarray(saved_full_times), fmt = "%s", delimiter= ",")
        np.savetxt(os.path.join(sys.path[0], "trading_daily_time_data.csv"), np.asarray(saved_daily_times), fmt = "%f", delimiter= ",")

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())

response = requests.get("https://www.marketwatch.com/investing/stock/tsla/options?mod=mw_quote_tab", timeout = 30)
soup = BeautifulSoup(str(response.text), 'html.parser')
price = soup.find_all("div", {"class": "container container--body"})[0]
price = price.find_all("div", {"class": "region region--primary"})[0]
price = price.find_all("div", {"class": "column column--full"})[0]
price = price.find_all("div", {"class": "accordion accordion--options"})[0]
price = price.find_all("mw-hybrid")[0]
price = price.find_all("ul", {"class": "tabs tabs--selection"})[0]
# for month in price: 
#     print(month.get_text())

#price = price.find_all("div", {"class": "accordion__item is-selected j-tabPane"})[0]
# price = price.find_all("div", {"class": "accordion__item j-tabPane"})[0]
#print(price)
# mod_len = len(price) - 1
# price = price[1:mod_len]
#print(len(price))
#price = price.find_all("div", {"class": "accordion__heading"})[0]
# price = price.find_all("div", {"class": "accordion__body j-tabBody"})[0]
# price = price.find_all("div", {"class": "element element--table"})[0]
# price = price.find_all("div", {"class": "wrapper"})[0]
# price = price.find_all("div", {"class": "overflow--table"})[0]
# price = price.find_all("table", {"class": "table table--overflow"})[0]
# price = price.find_all("tbody", {"class": "table__body"})[0]
# price = price.find_all("tr", {"class": "table__row"})[0]
# price = price[0]
# price = price.find_all("div", {"class": "accordion__body j-tabBody"})[0]
# price = price.find_all("div", {"class": "element element--table"})[0]
# price = price.find_all("div", {"class": "wrapper"})[0]
# price = price.find_all("div", {"class": "overflow--table"})[0]
# price = price.find_all("div", {"class": "intraday__data"})[0]
# price = price.find_all("h2", {"class": "intraday__price"})[0]
# price = price.find_all("bg-quote", {"class": "value"})[0].get_text()

response = requests.get("https://www.marketwatch.com/investing/stock/tsla/optionstable?optionMonth=May&optionYear=2023&partial=true", timeout = 30)
soup = BeautifulSoup(str(response.text), 'html.parser')
price = soup.find_all("div", {"class": "element element--table"})[0]
price = soup.find_all("div", {"class": "wrapper"})[0]
price = soup.find_all("div", {"class": "overflow--table"})[0]
price = soup.find_all("table", {"class": "table table--overflow"})
#print(price[0])

table_headers = ["Strike Price", "Last Trade Price", "Price Change Since Last Close", "Bid Price", "Ask Price", "Volume", "Open Interest", "Strike Price", "Last Trade Price", "Price Change Since Last Close", "Bid Price", "Ask Price", "Volume", "Open Interest"]

table_index = 0
stock = "TSLA"

for main_table in price:

    table_array = []
    #table_array.append(table_headers)

    table_body = main_table.find_all("tbody", {"class": "table__body"})[0] #gets all sub elements of table body
    rows = table_body.find_all("tr", {"class": "table__row"})
    
    first_row = rows[0]
    first_col = first_row.find_all("td", {"class": "l-show fixed--column"})[0]
    first_col = first_col.find_all("div", {"class": "option__cell strike"})[0].get_text()
    #print(first_col)

    for row in rows:
        row_array = []
        first_row = row
        first_col = first_row.find_all("td", {"class": "l-show fixed--column"})[0]
        val = first_col.find_all("div", {"class": "option__cell strike"})
        if val:
            first_col = val[0].get_text()
            #print(first_col)
            row_array.append(first_col)

        rest_cols = first_row.find_all("td")[1:]

        for col in rest_cols:
            cell = col.get_text()
            #print(cell)
            if cell:
                row_array.append(cell)
            else:
                row_array.append('0')
        #print(len(row_array))
        if len(row_array) == 14:
            table_array.append(row_array)


    table_array = np.array(table_array)
    # pd.DataFrame(table_array).to_csv(os.path.join(sys.path[0], f"options_data/{stock}_{expiry}.csv"), header = table_headers, index = None)
    pd.DataFrame(table_array).to_csv(os.path.join(sys.path[0], f"options_data/{stock}_{table_index}.csv"), header = table_headers, index = None)
    table_index += 1



    # for row in rows:
    #     #first_row = row[0]
    #     #val = row.find_all("td", {"class": "l-show fixed--column"})
    #     val = row.find_all("div", {"class": "option__cell strike"})
    #     if val:
    #         first_col = val[0].get_text()
    #         print(first_col)

    # first_row = table_body[0] #table__row 1
    #first_row = first_row[0]

    # first_col = first_row.find_all("div", {"class": "option__cell strike"})[0].get_text()
    #print(first_row)
    # print(first_col)
    # table = table.pop(0)
    # for row in table:
    #     for col in row:
    #         print(col)

#print(price)