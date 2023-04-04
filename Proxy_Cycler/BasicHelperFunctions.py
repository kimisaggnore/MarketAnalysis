import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import urllib.request , socket
import os
import sys
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

def retrieve_all_prices():
    prices_list = []
    all_companies = pd.read_csv(os.path.join(sys.path[0], "S&P500-Symbols.csv"))
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove('ABMD')
    all_companies.remove('CTXS')
    all_companies.remove('DRE')
    all_companies.remove('FBHS')
    all_companies.remove('NLSN')
    all_companies.remove('NLOK')
    all_companies.remove('TWTR')
    proxies_head = convert_list_to_linked_list(open(os.path.join(sys.path[0], "proxies.txt"), "r").read().strip().split("\n"))
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

def construct_symbols():
    all_companies = pd.read_csv(os.path.join(sys.path[0], "S&P500-Symbols.csv"))
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove('ABMD')
    all_companies.remove('CTXS')
    all_companies.remove('DRE')
    all_companies.remove('FBHS')
    all_companies.remove('NLSN')
    all_companies.remove('NLOK')
    all_companies.remove('TWTR')
    return all_companies


def fetch_price(soup):
    price = soup.find_all("div", {"class": "container container--body"})[0]
    price = price.find_all("div", {"class": "region region--intraday"})[0]
    price = price.find_all("div", {"class": "column column--aside"})[0]
    price = price.find_all("div", {"class": "element element--intraday"})[0]
    price = price.find_all("div", {"class": "intraday__data"})[0]
    price = price.find_all("h2", {"class": "intraday__price"})[0]
    price = price.find_all("bg-quote", {"class": "value"})[0].get_text()
    return price

def fetch_volume(soup):
    volume = soup.find_all("div", {"class": "container container--body"})[0]
    volume = volume.find_all("div", {"class": "region region--intraday"})[0]
    volume = volume.find_all("div", {"class": "column column--full supportive-data"})[0]
    volume = volume.find_all("mw-rangebar", {"class": "element element--range range--volume"})[0]
    volume = volume.find_all("div", {"class": "range__header"})[0]
    volume = volume.find_all("span", {"class": "primary"})[0].get_text()
    volume = volume.replace("Volume: ","")
    return volume

def fetch_volume_scale(soup):
    price = soup.find_all("div", {"class": "highcharts-container"})[0]

    return price


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
    return float(total)/float(length), list_of_remaining

def merge_lists(prev_data, cur_data, remaining_list):
    indexer_one = 0
    indexer_two = 0
    len_list1 = len(prev_data)
    len_list2 = len(cur_data)
    is_not_greater = True
    while is_not_greater:
        while indexer_one < len_list1 and prev_data[indexer_one] != 0:
            indexer_one += 1
        while indexer_two < len_list2 and cur_data[indexer_two] == 0:
            indexer_two += 1
        if indexer_one >= len_list1 or indexer_two >= len_list2:
            is_not_greater = False
            break
        prev_data[indexer_one] = cur_data[indexer_two]
        indexer_two += 1
    return prev_data

async def retrieve_data(session, url, proxy, return_prices, return_volumes, counter):
    try:
        async with session.get(url, proxy = f"http://{proxy.data}", ssl = False, timeout = 10) as res:
            if res.ok:
                response = await res.text()
                document_soup = BeautifulSoup(str(response), 'html.parser')
                price = fetch_price(document_soup)
                volume = fetch_volume(document_soup)
                return_prices[counter] = price
                return_volumes[counter] = volume
                return price
            else:
                return 0
    except:
        return 0

async def retrieve_SP_500_data(companies, proxies_head, all_companies):
    proxy = proxies_head
    return_prices = ['0']*len(companies)
    return_volumes = ['0']*len(companies)
    async with aiohttp.ClientSession() as session:
        tasks = []
        counter = 0
        for index in companies:
            if index == 1:
                url = f"https://www.marketwatch.com/investing/stock/{all_companies[counter]}?mod=search_symbol"
                tasks.append(asyncio.ensure_future(retrieve_data(session, url, proxy, return_prices, return_volumes, counter)))
                if proxy.next != None:
                    proxy = proxy.next
                else:
                    proxy = proxies_head
            counter += 1
        
        all_prices = await asyncio.gather(*tasks)
        return return_prices, return_volumes


async def check_proxy(session, proxy, return_proxies, counter):
    url = f"https://www.marketwatch.com/"
    try:
        async with session.get(url, proxy = f"http://{proxy}", ssl = False, timeout = 5) as res:
            if res.ok:
                response = await res.text()
                return_proxies[counter] = 1
                return 1
            else:
                return 0
    except:
        return 0

async def check_proxies(proxy_list):
    return_proxies = [0]*len(proxy_list)
    async with aiohttp.ClientSession() as session:
        tasks = []
        counter = 0
        for proxy in proxy_list:
            tasks.append(asyncio.ensure_future(check_proxy(session, proxy, return_proxies, counter)))
            counter += 1
        
        # global working_proxies
        working_proxies = await asyncio.gather(*tasks)
        return return_proxies