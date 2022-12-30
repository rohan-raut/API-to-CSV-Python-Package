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
        # print(key_list)
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
            # locate=locate+"-[]-"+locate_ret
            locate=locate+"-"+locate_ret
            return locate,found

    return "-1",False



def traverse(location_arr, index, data_list, data, target):
    # if(location_arr[index]==target):
        # print("done")
        # data_list.append(data[location_arr[index]])
        # return data_list

    if(type(data)==dict):
        temp = traverse(location_arr, index+1, data_list, data[location_arr[index]], target)
    elif(type(data)==list):
        for every_obj in data:
            temp = traverse(location_arr, index, data_list, every_obj, target)
            data_list = temp
    else:
        data_list.append(data)
        # return data_list
        
    return data_list




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

    # Collecting data in data_dic 
    data_dic={}
    for obj in records:
        data_dic[obj]=[]
        location_arr = location[obj].split("-")
        count=0
        for x in location_arr:
            if(x==''):
                count=count+1
        while(count):
            location_arr.remove('')
            count=count-1
        # print(location_arr)
        data_dic[obj] = traverse(location_arr, 0, [], data, obj)
        # print(location_arr)

    print(data_dic)
    # print(data)
    df=pd.DataFrame(data_dic)
    df.to_csv("sample.csv", index=False)

    



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



# get_df(api="https://api.openweathermap.org/data/2.5/weather?q=pune&units=metric&appid=b97e5c4f9b910fbc38bfe3ebf8f86020", records=["lon","lat","description"])
get_df(api="http://127.0.0.1:8000/api/ground-list", records=["ground_id","username","ground_name","city","area"])





























# Make a traversal function to traverse the location for each record - and when a list appears then start iterations








# Algorithms:
# Recurssion
# DFS
# Backtracking - to store data from json in array
# Dynamic Programming - to save time
