import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time

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
    #print(proxy.data)
    async with session.get(url, proxy = f"http://{proxy.data}", ssl = False) as res:
        if res.ok:
            response = await res.text()
            document_soup = BeautifulSoup(str(response), 'html.parser')
            price = fetch_price(document_soup)
            #print(price)
            return price
        else:
            return None


async def retrieve_SP_500_prices():
    proxy = proxies_head
    async with aiohttp.ClientSession() as session:

        tasks = []
        for company in all_companies:
            if proxy.next != None:
                proxy = proxy.next
            else:
                proxy = proxies_head
            url = f"https://www.marketwatch.com/investing/stock/{company}?mod=search_symbol"
            tasks.append(asyncio.ensure_future(retrieve_price(session, url, proxy)))
        
        all_prices = await asyncio.gather(*tasks)
        print(all_prices)

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
start_time = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(retrieve_SP_500_prices())
print("--- %s seconds ---" % (time.time() - start_time))






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
