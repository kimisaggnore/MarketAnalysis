from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
import os

def getpageHTML(url):
    response = requests.get(url)
    return response.text

def create_cash_flow_statement_URL(ticker, setting):
    if setting == "quarter":
        append = "/quarter"
    else:
        append = ""

    return f"https://www.marketwatch.com/investing/stock/{ticker}/financials/cash-flow{append}"

def save_html_page(ticker, setting):
    if setting == "quarter":
        append_2 = "_quarter"
    else:
        append_2 = "_annual"

    url = create_cash_flow_statement_URL(ticker, setting)
    document = getpageHTML(url)

    doucment_soup = BeautifulSoup(document, 'html.parser')
    with open(f"html_files/company_cash_flow_statements_html/saved_{ticker}_cash_flow_statement{append_2}.txt", "w", encoding = "utf-8") as file:
        file.write(str(doucment_soup))


def write_cash_flow_statement_to_csv(ticker, setting):

    if setting == "quarter":
        append = "_quarter"
    else:
        append = "_annual"

    with open(f'{append}_statements/company_cash_flow_statements{append}/{ticker}_cash_flow_statement{append}.csv', mode = "w", newline = '') as company_fundamental_valuation:
        company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

        company_profile = open(f"html_files/company_cash_flow_statements_html/saved_{ticker}_cash_flow_statement{append}.txt", "r")

        document_soup = company_profile.read()
        document_soup = BeautifulSoup(document_soup, 'html.parser')
        company_profile.close()
        
        for table in range(0,2):
            valuation_table = document_soup.find_all("div", {"class": "element element--table table--fixed financials"})[table].find_all("tr", {"class": "table__row"})
            
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
    path = "html_files/company_cash_flow_statements_html"
    dir_list = os.listdir(path)
    for fil in dir_list:
        new_fil = fil.replace("cash_flow_statement", "cash_flow_statement.txt")
        os.rename(f"html_files/company_cash_flow_statements_html/{fil}", f"html_files/company_cash_flow_statements_html/{new_fil}")

def list_all():
    path = "html_files/company_cash_flow_statements_html"
    dir_list = os.listdir(path)
    print(len(dir_list))

def update_all_cash_flow_statements(setting):
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
    if setting == "quarter":
        all_companies.remove("BBWI")
        all_companies.remove("CEG")
    index = 0
    for company in all_companies:
        print(f"{index}:{company}")
        write_cash_flow_statement_to_csv(company, setting)
        index += 1

def update_all_cash_flow_statements_html(setting):
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

#rename_all()
#update_all_cash_flow_statements_html("")
#update_all_cash_flow_statements("")

