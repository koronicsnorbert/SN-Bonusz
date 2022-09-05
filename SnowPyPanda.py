import requests
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import locale
from datetime import datetime, timedelta
import os


# Setups
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('mode.chained_assignment', None)
np.set_printoptions(suppress=True)
locale.setlocale( locale.LC_ALL, 'hu_HU.UTF-8')

load_dotenv('.env')

r=requests.get(os.getenv("SNurl"), auth=(os.getenv("SNuser"), os.getenv("SNpass")))
rawjson = json.loads(r.text)
df = pd.json_normalize(rawjson, record_path =['result']).replace(r'^s*$', float('NaN'), regex = True)
#print(df)
pivot = df[['resolved_by.display_value', 'number', 'calendar_duration','subcategory','u_sulyozas_mero']]
#print(pivot)
#print(pivot.dtypes)
pivot["u_sulyozas_mero"] = pivot["u_sulyozas_mero"].astype(float)
pivot["calendar_duration"] = pd.to_timedelta(pivot['calendar_duration'], unit='h', errors="coerce")
#pivot["business_calendar_duration"] = pivot["business_calendar_duration"].dt.total_seconds()


#print(pivot.dtypes)
# pivot["business_calendar_duration_sec"] = pivot["business_calendar_duration"].apply(lambda x: x.total_seconds())
#print(pivot)
df1 = pd.pivot_table(pivot,
                     index = ["resolved_by.display_value"],
                     values = ["u_sulyozas_mero","calendar_duration"],
                     aggfunc =dict(u_sulyozas_mero=np.sum, calendar_duration=np.mean))


df2 = df1.reset_index()
df2.columns = ['Név', 'Atlagos_Megoldasi_Ido', 'OsszSuly']
avg_suly = df2["OsszSuly"].mean().astype(float).astype(int)
maxatlagido = pd.Timedelta((os.getenv("Maxatlagido")))
df2["Teljesitmeny"] = df2.OsszSuly/avg_suly
df2["Bonus"] = np.where((df2['OsszSuly']>avg_suly) & (df2["Atlagos_Megoldasi_Ido"] < maxatlagido), df2.Teljesitmeny * int(os.getenv("Bonusz")), '0').astype(float).astype(int)
kinekbonusz = df2.loc[df2['Bonus'] > 0].astype(str) + ' Ft'



print("Bónusz feltételek: \n\n"
      "Havi átlag jegysúly: ",avg_suly,
      "\nMax átlag megoldási idő:", maxatlagido,
      "\nBónusz mértéke:",int(os.getenv("Bonusz")),"Ft",
      "\n\n Havi riport\n\n", df2[['Név', 'Atlagos_Megoldasi_Ido', 'OsszSuly']].sort_values(by='OsszSuly', ascending=False),
      "\n\n Bónuszra jogosultak:\n", kinekbonusz[['Név', 'Bonus']].sort_values(by='Bonus', ascending=False)
      )