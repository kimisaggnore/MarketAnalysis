import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import urllib.request , socket

class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


def get_page(url, proxy):
    response = requests.get(url, proxies = {"http": f"http://{proxy}"}, timeout = 30)
    if response.status_code >= 200 and response.status_code < 300:
        return (True, response.text)
    else:
        return (False, None)

def convert_list_to_linked_list(proxies):
    cur = ListNode(None)
    dummy_node = cur
    for proxy in proxies:
        cur.next = ListNode(proxy)
        cur = cur.next
    return dummy_node.next

def fetch_price(soup):
    price = soup.find_all("div", {"class": "container container--body"})[0]
    price = price.find_all("div", {"class": "region region--intraday"})[0]
    price = price.find_all("div", {"class": "column column--aside"})[0]
    price = price.find_all("div", {"class": "element element--intraday"})[0]
    price = price.find_all("div", {"class": "intraday__data"})[0]
    price = price.find_all("h2", {"class": "intraday__price"})[0]
    price = price.find_all("bg-quote", {"class": "value"})[0].get_text()
    return price

async def retrieve_price(session, url, proxy):
    try:
        async with session.get(url, proxy = f"http://{proxy.data}", ssl = False, timeout = 10) as res:
            if res.ok:
                response = await res.text()
                document_soup = BeautifulSoup(str(response), 'html.parser')
                price = fetch_price(document_soup)
                return price
            else:
                return 0
    except:
        return 0

async def retrieve_SP_500_prices(companies):
    proxy = proxies_head
    async with aiohttp.ClientSession() as session:
        tasks = []
        counter = 0
        for index in companies:
            if index == 1:
                url = f"https://www.marketwatch.com/investing/stock/{all_companies[counter]}?mod=search_symbol"
                tasks.append(asyncio.ensure_future(retrieve_price(session, url, proxy)))
                if proxy.next != None:
                    proxy = proxy.next
                else:
                    proxy = proxies_head
            counter += 1
        
        global all_prices
        all_prices = await asyncio.gather(*tasks)
        
async def check_proxy(session, proxy):
    url = f"https://www.marketwatch.com/"
    try:
        async with session.get(url, proxy = f"http://{proxy}", ssl = False, timeout = 6) as res:
            if res.ok:
                response = await res.text()
                return 1
            else:
                return 0
    except:
        return 0

async def check_proxies():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for proxy in proxy_list:
            tasks.append(asyncio.ensure_future(check_proxy(session, proxy)))
        
        global working_proxies
        working_proxies = await asyncio.gather(*tasks)

def check_num_successful(list_of_prices):
    list_of_remaining = []
    length = len(list_of_prices)
    total = 0
    for price in list_of_prices:
        if price != 0:
            total += 1
            list_of_remaining.append(0)
        else:
            list_of_remaining.append(1)
    print("\n")
    print(list_of_remaining)
    print("\n")
    return float(total)/float(length), list_of_remaining

def merge_prices_lists(prev_prices, cur_prices, remaining_list):
    indexer_one = 0
    indexer_two = 0
    len_list = len(prev_prices)
    is_not_greater = True
    while is_not_greater:
        while indexer_one < len_list and prev_prices[indexer_one] != 0:
            indexer_one += 1
        while indexer_two < len_list and cur_prices[indexer_two] == 0:
            indexer_two += 1
        prev_prices[indexer_one] = cur_prices[indexer_two]
        remaining_list[indexer_one] = 0
        if indexer_one >= len_list or indexer_two >= len_list:
            is_not_greater = False
    return prev_prices, remaining_list
    
all_companies = pd.read_csv("Proxy_Cycling/S&P500-Symbols.csv")
all_companies = all_companies.loc[:,"Symbol"]
all_companies = all_companies.tolist()
all_companies.remove('ABMD')
all_companies.remove('CTXS')
all_companies.remove('DRE')
all_companies.remove('FBHS')
all_companies.remove('NLSN')
all_companies.remove('NLOK')
all_companies.remove('TWTR')
proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
proxy_list = open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n")
# print(len(proxy_list))


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

start_time = time.time()
new_proxy_list = []
asyncio.run(check_proxies())
index = 0
for proxies in working_proxies:
    if proxies != 0:
        new_proxy_list.append(proxy_list[index])
    index += 1
print("--- %s seconds ---" % (time.time() - start_time))

proxies_head = convert_list_to_linked_list(new_proxy_list)
start_time = time.time()
indexes = [1]*120
asyncio.run(retrieve_SP_500_prices(indexes))
print(all_prices)
print("--- %s seconds ---" % (time.time() - start_time))

current_prices = all_prices.copy()
percent_success, remaining_list = check_num_successful(all_prices)
#while not percent_success >= .9:

asyncio.run(retrieve_SP_500_prices(remaining_list))
#percent_success, remaining_list = check_num_successful(all_prices)
print("--- %s seconds ---" % (time.time() - start_time))
print(current_prices)
print("\n")
print(all_prices)


    


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

# start_time = time.time()


# async def get_pokemon(session, url):
#     async with session.get("https://www.marketwatch.com/investing/stock/AAPL?mod=search_symbol") as resp:
#         pokemon = await resp.text()
#         return pokemon


# async def main():

#     async with aiohttp.ClientSession() as session:

#         tasks = []
#         for number in range(1, 151):
#             url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#             tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

#         original_pokemon = await asyncio.gather(*tasks)
#         for pokemon in original_pokemon:
#             print(pokemon)

# asyncio.run(main())
# print("--- %s seconds ---" % (time.time() - start_time))


def retrieve_all_prices():
    prices_list = []
    all_companies = pd.read_csv("Proxy_Cycling/S&P500-Symbols.csv")
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove('ABMD')
    all_companies.remove('CTXS')
    all_companies.remove('DRE')
    all_companies.remove('FBHS')
    all_companies.remove('NLSN')
    all_companies.remove('NLOK')
    all_companies.remove('TWTR')
    proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
    proxy = proxies_head
    # all_companies = all_companies[450:]
    for company in all_companies:
        if proxy != None:
            url = f"https://www.marketwatch.com/investing/stock/{company}?mod=search_symbol"
            res = get_page(url, proxy)
            num_cycles = 1
            while not res[0]:
                proxy = proxy.next
                if proxy == None:
                    break
                res = get_page(url, proxy)
                num_cycles += 1
            #print(num_cycles)
            document_soup = BeautifulSoup(str(res), 'html.parser')
            #print(fetch_price(document_soup))
            cur_price = fetch_price(document_soup)
            prices_list.append(cur_price)
            print(cur_price)
            proxy = proxy.next
        else:
            proxy = proxies_head

    #return prices_list

#retrieve_all_prices()
