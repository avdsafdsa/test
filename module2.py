import yfinance as yf
import pandas as pd
import requests 
import io
import math
url = "https://www.iposcoop.com/ipos-recently-filed/"
response = requests.get(url)


company_name_type_dict = {

    "Technologies" : "Technologies",
    "Acquisition Corp"  : "Acquisition Corp",
    "Acquisition Corporation"  : "Acquisition Corp",
    "Corp" : "Acquisition Corp",
    "Inc"  : "Inc.",
    "Incorporated" : "Inc.",
    "Group" : "Group",
    "Ltd"   : "Limited",
    "Limited" :"Limited",
    "Holdings" : "Holdings",
    "Holding" : "Holdings",
    "Others" : "Other"
}

def parse_float(val1):
    try:
         val = str(val1)
         return float(val.replace("$", "").replace(",", "").strip())
    except ValueError:     
        return math.nan





df = pd.read_html(io.StringIO(response.text))[0]



df["File Date"] = pd.to_datetime(df["File Date"])
df = df[(df["Expected To Trade"] == "Withdrawn") & (df["File Date"] < pd.to_datetime("2026-09-11"))]
df["Company Type"]= df.apply(lambda row: 
                             company_name_type_dict.get(next( (k.strip(".") for k in  row["Company"].split() if k.strip(".") in company_name_type_dict),None), "Other"),  axis=1)


df["Avg_price"] = df.apply(lambda row: parse_float(row["Price Low"]) + parse_float(row["Price High"])   / 2, axis=1)

df["Shares (millions)"] = df.apply(lambda row: parse_float(row["Shares (millions)"]), axis=1)
df["Est $ Vol (millions)"] = df.apply(lambda row: parse_float(row["Est $ Vol (millions)"]), axis=1)

df["Shares_offered_value"] = df.apply(lambda row: row["Shares (millions)"] * row["Avg_price"] if not math.isnan(row["Shares (millions)"] * row["Avg_price"]) else row["Est $ Vol (millions)"], axis=1)


print(df[[ "Company Type" ,"Avg_price" ,"Shares (millions)", "Est $ Vol (millions)", "Shares_offered_value"]])


print(df.groupby("Company Type").sum(numeric_only=True)[["Shares_offered_value"]])