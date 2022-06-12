import requests
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os


# Setups
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('mode.chained_assignment', None)
load_dotenv('.env')  # take environment variables from .env.

r=requests.get(os.getenv("SNurl"), auth=(os.getenv("SNuser"), os.getenv("SNpass")))
rawjson = json.loads(r.text)

df = pd.json_normalize(rawjson, record_path =['result']).replace(r'^s*$', float('NaN'), regex = True)
#print(df)
pivot = df[['resolved_by.display_value', 'number', 'business_duration','subcategory','u_sulyozas_mero']]
#print(pivot)

pivot["u_sulyozas_mero"] = pivot["u_sulyozas_mero"].astype(float)
pivot["business_duration"] = pd.to_timedelta(pivot['business_duration'])


print(pd.pivot_table(pivot,
                     index = ["resolved_by.display_value"],
                     values = ["u_sulyozas_mero","business_duration"],
                     aggfunc =dict(u_sulyozas_mero=np.sum, business_duration=np.mean)))

