import requests

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
    dummy_node = ListNode(None)
    for proxy in proxies:
        cur.next = ListNode(proxy)
        cur = cur.next
    return dummy_node.next


proxies_head = convert_list_to_linked_list(open("Proxy_Cycling/proxies.txt", "r").read().strip().split("\n"))
test_url = "https://www.marketwatch.com/"


num_cycles = 1
proxy = proxies_head
res = get_page(test_url, proxy)
print(num_cycles)
while not res[0]:
    if num_cycles != 1:
        prev.next = proxy.next
    prev = proxy
    proxy = proxy.next
    if proxy == None:
        break
    res = get_page(test_url, proxy)
    num_cycles += 1
    print(num_cycles)



#print(proxies)
