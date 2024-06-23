import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

def F_list_files(folder_path):
#Function to see all data files in a given folder
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
#Function to import data as dataframe from given location and its index as 'ind'
    x=F_list_files(loc)
    if x[ind][3]=='xlsx':
        df = pd.read_excel(x[ind][1]+'/'+x[ind][2])
    elif x[ind][3]=='csv':
        df = pd.read_csv(x[ind][1]+'/'+x[ind][2])
    elif x[ind][3]=='xls':
        df = pd.read_excel(x[ind][1]+'/'+x[ind][2])
    return df

def F_check_data(data):
#Function to check a dataframe: Data type, total values, missing values, unique values
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
#Function to remove duplicates
    df=data.drop_duplicates(subset=key, keep='first')
    print(len(data), len(df))
    return df

def F_gen_date(df,col,start_date, end_date):

    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Generate a list of random dates
    date_range = (end_date - start_date).days
    random_dates = [start_date + timedelta(days=np.random.randint(0, date_range)) for _ in range(len(df))]
    
    # Add the "date of birth" column to the DataFrame
    df[col] = random_dates
    return df

def Fx_dt2str(df, column_name, date_format='%Y-%m-%d'):

    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    # Convert the date column to string format
    df[column_name] = df[column_name].dt.strftime(date_format)
    return df

def Fx_str2dt(df, column_name, date_format='%Y-%m-%d'):
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    # Convert the string column to date format
    df[column_name] = pd.to_datetime(df[column_name], format=date_format)
    return df
