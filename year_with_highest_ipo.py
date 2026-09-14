import pandas as pd
import requests
from datetime import datetime  as dt
from io import StringIO


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Fetch the HTML content with headers
response = requests.get(url, headers=headers)


tables = pd.read_html(StringIO(response.text))
df=tables[0]


df["Date added"] = pd.to_datetime(df["Date added"])
df["yearAdded"] = df["Date added"].dt.year


currYear=dt.now().year
overThanYearsCount=20
print(df[(df["yearAdded"]>=2020)&(df["yearAdded"]< currYear)]["yearAdded"] .max())

print(df[(df["yearAdded"]<currYear-overThanYearsCount)]["Symbol"] .count())

#Q2

benchmark ="%5EGSPC" 
indicies =[benchmark,"%5ENSEI", "%5EAXJO","%5EHSI","000001.SS","%5EBVSP","%5EMXX","%5EN225","%5EGDAXI","%5EGSPTSE"]#,"%5EFTSE"]
result = {}
for index_name in indicies:

    url=f"https://finance.yahoo.com/quote/{index_name}/history/?period1=1767225600&period2=1789420714"
    response = requests.get(url, headers=headers)
    print(url)
    tables = pd.read_html(StringIO(response.text))
    df=tables[0]
    df.columns.values[4]="Close"
    #print(df.head().to_string())
    df["Date"] = pd.to_datetime(df["Date"])
    open = df.loc[df["Date"].idxmin()]["Open"]
    close = df.loc[df["Date"].idxmax()]["Close"]
    change = (close-open)/open
    result[index_name]=change

print(result)

benchmark_value = result[benchmark]
print(sum( v> benchmark_value for k,v in result.items()))



#https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md
#https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md
#https://courses.datatalks.club/sma-zoomcamp-2026/