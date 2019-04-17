import requests
import psutil
import time
import json
import pandas
import datetime
import datetime as dt
import pdb

hit_url = "http://localhost/logs/add"
df = pandas.read_csv("scripts/webLog.csv")
#pdb.set_trace()
for index, each in df.iterrows():
    try:
        if each["Time"]=="cannot": continue
        source_ip = each["IP"]
        print(source_ip)
        date_time = datetime.datetime.strptime(each["Time"], "[%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        print(date_time)
        url = str(each["URL"]).split(" ")
        uri = url[1]
        print(uri)
        request_type = url[0]
        print(request_type)
        status_code = int(each["Staus"])
        print(status_code)
        server_name = "server 1"
        try:
            #r = requests.post(hit_url, json={"server_name": server_name, "source_ip": source_ip, "date_time": date_time, "uri": uri, "request_type": request_type, "status_code": status_code})
            print(json.dumps(r.json()))
        except Exception as ex:
            print("exception is ", ex)
        print("------")
    except Exception as ex:
        #print each
        #pdb.set_trace()
        pass