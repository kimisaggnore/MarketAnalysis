from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
import os
import sys

def get_page_HTML(url):
    response = requests.get(url)
    return response.text

def create_income_statement_URL(ticker, setting):
    if setting == "quarter":
        append = "/quarter"
    else:
        append = ""

    return f"https://www.marketwatch.com/investing/stock/{ticker}/financials/income{append}"

def save_html_page(ticker, setting):

    if setting == "quarter":
        append = "/quarter"
        append_2 = "_quarter"
    else:
        append = ""
        append_2 = "_annual"

    url = create_income_statement_URL(ticker, setting)
    #print(ticker)
    document = get_page_HTML(url)

    document_soup = BeautifulSoup(document, 'html.parser')

    with open(pd.read_csv(os.path.join(sys.path[0],f"html_files/company_income_statements_html/saved_{ticker}_income_statement{append_2}.txt")), "w") as file:
        file.write(str(document_soup))
    
def write_income_statement_to_csv(ticker, setting):

    if setting == "quarter":
        append = "/quarter"
        append_2 = "_quarter"
    else:
        append = ""
        append_2 = "_annual"

    with open(os.path.join(sys.path[0],f'{append_2}_statements/company_income_statements{append_2}/{ticker}_income_statement{append_2}.csv'), mode = "w", newline = '') as company_fundamental_valuation:
        company_fundamental_valuation_write = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

        company_profile = open(os.path.join(sys.path[0],f"html_files/company_income_statements_html/saved_{ticker}_income_statement{append_2}.txt"), "r")

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
    path = os.path.join(sys.path[0],"company_balance_sheets_html")
    dir_list = os.listdir(path)
    for fil in dir_list:
        new_fil = fil.replace("balance_sheet.txt", "balance_sheet")
        os.rename(os.path.join(sys.path[0],f"company_balance_sheets_html/{fil}"), os.path.join(sys.path[0],f"company_balance_sheets_html/{new_fil}"))


def update_all_income_statements(setting):
    all_companies = pd.read_csv(os.path.join(sys.path[0],"S&P500-Info.csv"))
    all_companies = all_companies.loc[:,"Symbol"]
    all_companies = all_companies.tolist()
    all_companies.remove("MMM")
    all_companies.remove('AMCR')
    all_companies.remove('EVRG')
    all_companies.remove('MTCH')
    index = 0
    for company in all_companies:
        print(f"{index}:{company}")
        write_income_statement_to_csv(company, setting)
        index += 1
    #rename_all()

def update_all_income_statements_html(setting):
    all_companies = pd.read_csv(os.path.join(sys.path[0],"S&P500-Info.csv"))
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

#update_all_income_statements_html("quarter")
update_all_income_statements("quarter")