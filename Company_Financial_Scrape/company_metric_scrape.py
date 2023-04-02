from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 


def get_page_HTML(url):
    response = requests.get(url)
    return response.text

def createProfileURL(ticker):
    return f"https://www.marketwatch.com/investing/stock/{ticker}/company-profile?mod=mw_quote_tab"

def append_company_valuation(ticker):

    url = createProfileURL(ticker)
    print(ticker)
    document = get_page_HTML(url)
    document_soup = BeautifulSoup(document, 'html.parser')
    valuation_table = document_soup.find_all("tr", {"class": "table__row"})
    valuation_table = valuation_table[10:39]
    #print(valuation_table)
    valuation_values_array = []
    valuation_values_array.append(ticker)
    if len(valuation_table[0].find_all("td", {"class": "table__cell w75"})) > 0:
        for sub_table in range(0,29):
            if len(valuation_table[sub_table].find_all("td", {"class": "table__cell w25"})) > 0:
                valuation = valuation_table[sub_table].find_all("td", {"class": "table__cell w25"})[0].get_text()
                valuation_values_array.append(valuation)
            else:
                valuation = "N/A"
                valuation_values_array.append(valuation)

        with open(os.path.join(sys.path[0],'company_fundamental_valuation_2.csv'), mode = "a", newline = '') as company_fundamental_valuation:
            company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            company_fundamental_valuation_write.writerow(valuation_values_array)
    else:
        with open(os.path.join(sys.path[0],'company_fundamental_valuation_2.csv'), mode = "a", newline = '') as company_fundamental_valuation:
            company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            valuation_values_array = ["N/A"]*29
            company_fundamental_valuation_write.writerow(valuation_values_array)


# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# df = table[0]
# df.to_csv('S&P500-Info.csv')
# df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

all_companies = pd.read_csv("S&P500-Info.csv")
all_companies = all_companies.loc[:,"Symbol"]
all_companies = all_companies.tolist()

with open('company_fundamental_valuation_2.csv', mode = "w", newline = '') as company_fundamental_valuation:
    company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    company_fundamental_valuation_write.writerow(['Company Tickers','P/E Current', 'P/E Ratio (w/ extraordinary items)', 'P/E Ratio (w/o extraordinary items)',
    'Price to Sales Ratio', 'Price to Book Ratio', 'Price to Cash Flow Ratio', 'Enterprise Value to EBITDA', 'Enterprise Value to Sales', 
    'Total Debt to Enterprise Value', 'Revenue/Employee', 'Income Per Employeee', 'Receivables Turnover', 'Total Asset Turnover', 'Current Ratio', 
    'Quick Ratio', 'Cash Ratio', 'Gross Margin', 'Operating Margin', 'Pretax Margin', 'Net Margin', 'Return on Assets', 'Return on Equity', 
    'Return on Total Capital', 'Return on Invested Capital', 'Total Debt to Total Equity', 'Total Debt to Total Capital', 'Total Debt to Total Assets', 
    'Long-Term Debt to Equity', 'Long-Term Debt to Total Capital'])

    #company_fundamental_valuation.close()
for company in all_companies:
    append_company_valuation(company)


