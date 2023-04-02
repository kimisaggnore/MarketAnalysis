from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
import os

def getpageHTML(url):
    response = requests.get(url)
    return response.text

def create_balance_sheet_URL(ticker, setting):

    if setting == "quarter":
        append = "/quarter"
    else:
        append = ""

    return f"https://www.marketwatch.com/investing/stock/{ticker}/financials/balance-sheet{append}"


def save_html_page(ticker, setting):

    if setting == "quarter":
        append = "/quarter"
        append_2 = "_quarter"
    else:
        append = ""
        append_2 = "_annual"
    
    url = create_balance_sheet_URL(ticker, setting)
    document = getpageHTML(url)
    document_soup = BeautifulSoup(document, 'html.parser')
    with open(f"html_files/company_balance_sheets_html/saved_{ticker}_balance_sheet{append_2}.txt", "w") as file:
        file.write(str(document_soup))
    

def append_company_balance_sheet(ticker):

    url = create_balance_sheet_URL(ticker)
    document = getpageHTML(url)
    document_soup = BeautifulSoup(document, 'html.parser')
    valuation_table = document_soup.find_all("div", {"class": "element element--table table--fixed financials"})[0].find_all("tr", {"class": "table__row"})
    for row in valuation_table:
        print("new row")
        print(row.find_all("div", {"class": "cell__content"}))
       
def write_balance_sheet_to_csv(ticker, setting):

    if setting == "quarter":
        append = "/quarter"
        append_2 = "_quarter"
    else:
        append = ""
        append_2 = "_annual"

    with open(f'{append_2}_statements/company_balance_sheets{append_2}/{ticker}_balance_sheet{append_2}.csv', mode = "w", newline = '') as company_fundamental_valuation:
        company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

        company_profile = open(f"html_files/company_balance_sheets_html/saved_{ticker}_balance_sheet{append_2}.txt", "r")

        document_soup = company_profile.read()
        document_soup = BeautifulSoup(document_soup, 'html.parser')
        company_profile.close()
        valuation_table = document_soup.find_all("div", {"class": "element element--table table--fixed financials"})[0].find_all("tr", {"class": "table__row"})

        for row in valuation_table:
            company_fundamental_valuation_write.writerow([
            row.find_all("div", {"class": "cell__content"})[1].get_text(),
            row.find_all("div", {"class": "cell__content"})[2].get_text(),
            row.find_all("div", {"class": "cell__content"})[3].get_text(),
            row.find_all("div", {"class": "cell__content"})[4].get_text(),
            row.find_all("div", {"class": "cell__content"})[5].get_text(),
            row.find_all("div", {"class": "cell__content"})[6].get_text(),
                                                        ])

def rename_all():
    path = "html_files/company_balance_sheets_html"
    dir_list = os.listdir(path)
    for fil in dir_list:
        new_fil = fil.replace("balance_sheet.txt", "balance_sheet")
        os.rename(f"company_balance_sheets_html/{fil}", f"company_balance_sheets_html/{new_fil}")

def update_all_balance_sheets(setting):
    all_companies = pd.read_csv("S&P500-Info.csv")
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove("MMM")
    all_companies.remove('AMCR')
    all_companies.remove('EVRG')
    all_companies.remove('MTCH')
    all_companies.remove('ABMD')
    all_companies.remove('CTXS')
    all_companies.remove('FBHS')
    all_companies.remove('LIN')
    all_companies.remove('NLSN')
    all_companies.remove('SIVB')
    all_companies.remove('TWTR')
    index = 0
    for company in all_companies[441:]:
        print(f"{index}:{company}")
        write_balance_sheet_to_csv(company, setting)
        index += 1

def update_all_balance_sheets_html(setting):
    all_companies = pd.read_csv("S&P500-Info.csv")
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove("MMM")
    all_companies.remove('AMCR')
    all_companies.remove('EVRG')
    all_companies.remove('MTCH')
    index = 0
    for company in all_companies:
        print(f"{index}:{company}")
        save_html_page(company, setting)
        index += 1

#update_all_balance_sheets_html("")
update_all_balance_sheets("")