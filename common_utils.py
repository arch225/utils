import pandas as pd
import os

def F_list_files(folder_path):
    file_list = []
    i=-1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext=file.split('.')[-1]
            if ext in ['xlsx', 'csv', 'xls']:
                i+=1
                file_list.append([i, root, file, ext])
#list_files('/Users/dibbi/Desktop/rac_utils')
    return file_list

def F_data_import(loc,ind):
    x=F_list_files(loc)
    if x[ind][3]=='xlsx':
        df = pd.read_excel(x[ind][1]+'/'+x[ind][2])
    elif x[ind][3]=='csv':
        df = pd.read_csv(x[ind][1]+'/'+x[ind][2])
    elif x[ind][3]=='xls':
        df = pd.read_excel(x[ind][1]+'/'+x[ind][2])
    return df

def F_check_data(data):
    col=list(data.columns)
    all_dtyp_lst=[]
    all_val_lst=[]
    uni_val_lst=[]
    per_fill_lst=[]
    miss_val_lst=[]
    per_miss_lst=[]
    for i in col:
        all_dtyp=data[i].dtypes
        all_val=len(data[i])
        uni_val=(data[i].nunique())
        per_fill=100*uni_val/all_val
        miss_val=(data[i].isnull().sum())
        per_miss=100*miss_val/all_val
        all_dtyp_lst.append(all_dtyp)
        all_val_lst.append(all_val)
        uni_val_lst.append(uni_val)
        per_fill_lst.append(per_fill)
        miss_val_lst.append(miss_val)
        per_miss_lst.append(per_miss)
    df_explore=pd.DataFrame({"Column":col,"Data Type":all_dtyp_lst,"Total Values":all_val_lst,"Unique Values":uni_val_lst,"Percentage of Filled Values":per_fill_lst,"Missing Values":miss_val_lst,"Percentage of Missing Values":per_miss_lst})
    return df_explore

def F_nodup(data,key):
    df=data.drop_duplicates(subset=key, keep='first')
    print(len(data), len(df))
    return df
