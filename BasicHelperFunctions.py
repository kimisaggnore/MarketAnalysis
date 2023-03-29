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

def construct_symbols():
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
        if indexer_one >= len_list or indexer_two >= len_list:
            is_not_greater = False
            break
        prev_prices[indexer_one] = cur_prices[indexer_two]
        remaining_list[indexer_one] = 0
    return prev_prices, remaining_list
