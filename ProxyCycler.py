import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    all_companies = all_companies[450:]
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
            prices_list.append(fetch_price(document_soup))
            proxy = proxy.next
        else:
            proxy = proxies_head
  
        print(company)
    return prices_list


retrieve_all_prices()
# num_cycles = 1
# proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
# proxy = proxies_head
# test_url = "https://www.marketwatch.com/investing/stock/enph?mod=search_symbol"
# res = get_page(test_url, proxy)
# print(num_cycles)
# while not res[0]:
#     proxy = proxy.next
#     if proxy == None:
#         break
#     res = get_page(test_url, proxy)
#     num_cycles += 1
#     print(num_cycles)


# document_soup = BeautifulSoup(str(res), 'html.parser')

# print(fetch_price(document_soup))


#[0].find_all("tr", {"class": "table__row"})

#print(proxies)
