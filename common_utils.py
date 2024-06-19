import pandas as pd
import os

def list_files(folder_path):
    file_list = []
    i=-1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext=file.split('.')[-1]
            if ext in ['xlsx', 'csv', 'xls']:
                i+=1
                file_list.append([i, root, file, ext])
    return file_list
