import requests
import json

### - Incidens Table API SNurl = "https://auchanhu.service-now.com/api/now/table/incident?sysparm_query=resolved_atONLast%20month%40javascript%3Ags.beginningOfLastMonth()%40javascript%3Ags.endOfLastMonth()%5Eassigned_to.manager%3Db7302538dba9b410d3640342f3961997%5Eassignment_group%3D6c37d064db2acb0072522de74b961918&sysparm_limit=1"
SNurl = "https://auchanhu.service-now.com/api/now/table/incident?sysparm_query=resolved_atONLast%20month%40javascript%3Ags.beginningOfLastMonth()%40javascript%3Ags.endOfLastMonth()%5Eassigned_to.manager%3Db7302538dba9b410d3640342f3961997%5Eassignment_group%3D6c37d064db2acb0072522de74b961918&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_limit=10"
SNuser = "norbert.koronics"
SNpass = "Auchan88!!"

r=requests.get(SNurl, auth=(SNuser, SNpass))
rawjson = r.json()
preaty_json = json.dumps(r.json(), indent=2)
#print(preaty_json)
#for tickets in rawjson["result"]:
#    print(tickets["resolved_by"][0]["number"])
print(rawjson["result"][0]["number"]["resolved_by"])