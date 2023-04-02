
import numpy as np
import csv 
import pandas as pd

metrics = ['Company Tickers','P/E Current', 'P/E Ratio (w/ extraordinary items)', 'P/E Ratio (w/o extraordinary items)',
    'Price to Sales Ratio', 'Price to Book Ratio', 'Price to Cash Flow Ratio', 'Enterprise Value to EBITDA', 'Enterprise Value to Sales', 
    'Total Debt to Enterprise Value', 'Revenue/Employee', 'Income Per Employeee', 'Receivables Turnover', 'Total Asset Turnover', 'Current Ratio', 
    'Quick Ratio', 'Cash Ratio', 'Gross Margin', 'Operating Margin', 'Pretax Margin', 'Net Margin', 'Return on Assets', 'Return on Equity', 
    'Return on Total Capital', 'Return on Invested Capital', 'Total Debt to Total Equity', 'Total Debt to Total Capital', 'Total Debt to Total Assets', 
    'Long-Term Debt to Equity', 'Long-Term Debt to Total Capital']

healthy_companies = []
metric_dict_less = {1:15, 4:4, 5:3, 6:14, 28:50, 29:40}
metric_dict_more = {14: 1.5, 20:20, 21:10,  22:12, 23:20, 24:20}


# with open('company_fundamental_valuation_copy.csv', mode = "w", newline = '') as company_fundamental_valuation:
#     company_fundamental_valuation_writer = csv.writer(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
#     for company in company_fundamental_valuation_writer:
#         for cell in company:
#             cell.replace("%", "")

#df = pd.read_csv("company_fundamental_valuation_copy.csv")

# inputfile = csv.reader(open('company_fundamental_valuation.csv','r'))
# outputfile = open('company_fundamental_valuation_copy.csv','w')

# i=0

# for row in inputfile:
#     place = row[2].replace('%','')
#     outputfile.write(place+'\n')
#     i+=1

with open(os.path.join(sys.path[0],'company_profiles/company_fundamental_valuation_copy.csv'), mode = "r", newline = '') as company_fundamental_valuation:
    company_fundamental_valuation_reader = csv.reader(company_fundamental_valuation, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    next(company_fundamental_valuation_reader)
    for company in company_fundamental_valuation_reader:
        if company[0] != "N/A":
            track_metric = [0]*12
            count = 0
            #print(company[0])
            for metric in metric_dict_less:
                if company[metric] != "N/A" and float(company[metric]) <= metric_dict_less[metric]:
                    track_metric[count] = True
                else: 
                    track_metric[count] = False
                count += 1
                
            for metric in metric_dict_more:
                if company[metric] != "N/A"  and float(company[metric]) >= metric_dict_more[metric]:
                    track_metric[count] = True
                else: 
                    track_metric[count] = False
                count += 1
            if np.count_nonzero(track_metric) >= (4/8)*len(track_metric):
                healthy_companies.append(company[0])
            #print(track_metric)
        

print(healthy_companies)

            
