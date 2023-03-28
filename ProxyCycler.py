import requests
from bs4 import BeautifulSoup

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

# prox = proxies_head
# while prox != None:
#     print(prox.data)
#     prox = prox.next

test_url = "https://www.marketwatch.com/investing/stock/enph?mod=search_symbol"


num_cycles = 1
proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
proxy = proxies_head
res = get_page(test_url, proxy)
#print(res[1])
print(num_cycles)
while not res[0]:
    proxy = proxy.next
    if proxy == None:
        break
    res = get_page(test_url, proxy)
    num_cycles += 1
    print(num_cycles)


document_soup = BeautifulSoup(str(res), 'html.parser')

print(fetch_price(document_soup))

#[0].find_all("tr", {"class": "table__row"})

#print(proxies)
