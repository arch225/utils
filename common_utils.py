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
