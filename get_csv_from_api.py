from operator import index
import requests
import json
import pandas as pd
from datetime import datetime
from requests.structures import CaseInsensitiveDict
from requests.models import Response
from get_json import get_json
import time


def get_location(data,record,locate,found):
    # print(type(data))
    if(type(data)==dict):
        key_list = list(data.keys())
        print(key_list)
        # print(record)
        if record in key_list:
            # print(record)
            found=True
            return locate+"-"+record,found
        else:
            for key in key_list:
                # if(type(data[key])==dict):
                locate_ret,found = get_location(data[key],record,locate,found)
                if(found):
                    locate=locate+"-"+key+"-"+locate_ret
                    return locate,found
    elif(type(data)==list):
        # print(data)
        locate_ret,found = get_location(data[0],record,locate,found)
        if(found):
            locate=locate+"-[]-"+locate_ret
            return locate,found


    return "-1",False



def get_df(api, token=None, records=[], header=None, outputFileName=None):
    if(token==None):
        resp = get_json(api=api)
    else:
        resp = get_json(api=api,token=token)

    # print(type(resp.text))

    data = json.loads(resp.text)

    location={}
    for obj in records:
        location[obj]=""
    
    for record in records:
        location[record]=get_location(data, record, "", False)[0]

    print(location)


    # if(len(records) != 0):
    #     mx_len = 1
    #     for obj in records:
    #         if(type(obj)==list):
    #             mx_len = max(mx_len,len(obj))

    #     dic = {}
    #     if header is not None:
    #         for colname in header:
    #             dic[colname]=[]
    #     else:
    #         for x in range(0,len(records)):
    #             dic[x]=[]
        
    #     keys = dic.keys()
    #     record_no=0
    #     for key in keys:
    #         if(records[record_no] != list):
    #             dic[key]=pd.Series([records[record_no]]*mx_len)
    #         else:
    #             dic[key]=records[record_no]
    #         record_no=record_no+1
        
    #     df = pd.DataFrame(dic, header=header)

    #     if outputFileName is not None:
    #         df.to_csv(outputFileName, index=False)
    #     else:
    #         milliseconds = int(round(time.time() * 1000))
    #         outputFileName = "output_"+milliseconds
    #         df.to_csv(outputFileName, index=False)



get_df(api="https://api.openweathermap.org/data/2.5/weather?q=pune&units=metric&appid=b97e5c4f9b910fbc38bfe3ebf8f86020", records=["icon","temp","main"])