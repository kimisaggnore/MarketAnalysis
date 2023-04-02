import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import urllib.request , socket

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

async def retrieve_SP_500_prices(companies, proxies_head, all_companies):
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
        
        all_prices = await asyncio.gather(*tasks)
        return all_prices


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

async def check_proxies(proxy_list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for proxy in proxy_list:
            tasks.append(asyncio.ensure_future(check_proxy(session, proxy)))
        
        # global working_proxies
        working_proxies = await asyncio.gather(*tasks)
        return working_proxies