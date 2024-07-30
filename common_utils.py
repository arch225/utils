import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from geopy.geocoders import Nominatim
import folium


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
def Fx_num2str(df, column_name):
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")    
    # Convert the number column to string format
    df[column_name] = df[column_name].astype(str)
    return df
def Fx_str2num(df, column_name):
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    # Convert the string column to numeric, coercing errors to NaN
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

def F_latnlong(address):
#Function to extract lat long of an address
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

def F_geo_map(address,zoom=4):
#Function to locate the address in a map
    x=F_latnlong(address)
    mymap = folium.Map(location=x, zoom_start=zoom)
    folium.Marker(x).add_to(mymap)
    mymap.save('map.html')
    return mymap

def F_df_info(df):
#function similar to F_check_data
    dat_info=pd.DataFrame({
    'column_name':df.columns.to_list(),
    'data_type':df.dtypes.to_list(),
    'null_count':df.isnull().sum().to_list(),
    'unique_count':df.nunique().to_list(),
    'total_count':[len(df[x]) for x in df.columns]})
    return dat_info

def fak_dat_gen(n):
    from faker import Faker
# Create a Faker instance
    fake = Faker()

# Initialize lists to store the data
    names = []
    emails = []
    ssns = []
    phone_numbers = []
    dates_of_birth = []
    incomes = []

# Generate 1000 rows of data
    for _ in range(n):
        name = fake.name()
        email = fake.email()
        ssn = fake.ssn()
        phone_number = fake.phone_number()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)
        income = fake.pydecimal(left_digits=5, right_digits=2, positive=True)

        names.append(name)
        emails.append(email)
        ssns.append(ssn)
        phone_numbers.append(phone_number)
        dates_of_birth.append(date_of_birth)
        incomes.append(income)

# Create a DataFrame from the lists
    data = pd.DataFrame({
        'Name': names,
        'Email': emails,
        'SSN': ssns,
        'Phone Number': phone_numbers,
        'Date of Birth': dates_of_birth,
        'Income': incomes
    })
    return data

def F_danon_email(df,id,pii_col):
    lst=[id,pii_col]
    df1=df[lst]
    print('Masking started for',pii_col,'.......')
    # Remove duplicates in-place
    df2=df1.drop_duplicates(subset=lst)
    df2.drop(pii_col,axis=1,inplace=True)

    email_lst_fk=[]
    for x in range(len(df2)):
        email=fake.unique.email()
        email_lst_fk.append(email)
    df2[pii_col]=email_lst_fk
    #Merging with Original data
    input_data=df.drop(columns=[pii_col])
    out_data=input_data.merge(df2,how='left',on=id)
    print('Masking completed for',pii_col,'for ',len(email_lst_fk),' emails')
    #To maintain same order of column as input var
    lt=df.columns.to_list()
    out_data=out_data[lt]
    # F_danon_email(input_df,id='Unnamed: 0',pii_col='Email')
    return out_data


def F_danon_fname(df,id,pii_col):
    lst=[id,pii_col]
    df1=df[lst]
    print('Masking started for',pii_col,'.......')
    # Remove duplicates in-place
    df2=df1.drop_duplicates(subset=lst)
    df2.drop(pii_col,axis=1,inplace=True)

    lst_fk=[]
    for x in range(len(df2)):
        mask_data=fake.first_name()
        lst_fk.append(mask_data)
    df2[pii_col]=lst_fk
    #Merging with Original data
    input_data=df.drop(columns=[pii_col])
    out_data=input_data.merge(df2,how='left',on=id)
    print('Masking completed for',pii_col,'for ',len(lst_fk),' names')
    #To maintain same order of column as input var
    lt=df.columns.to_list()
    out_data=out_data[lt]
    # F_danon_fname(input_df,id='Unnamed: 0',pii_col='Name')
    return out_data

def F_danon_phn(df,id,pii_col):
    lst=[id,pii_col]
    df1=df[lst]
    print('Masking started for',pii_col,'.......')
    # Remove duplicates in-place
    df2=df1.drop_duplicates(subset=lst)
    df2.drop(pii_col,axis=1,inplace=True)

    lst_fk=[]
    for x in range(len(df2)):
        mask_data=fake.phone_number()
        lst_fk.append(mask_data)
    df2[pii_col]=lst_fk
    #Merging with Original data
    input_data=df.drop(columns=[pii_col])
    out_data=input_data.merge(df2,how='left',on=id)
    print('Masking completed for',pii_col,'for ',len(lst_fk),' phones')
    #To maintain same order of column as input var
    lt=df.columns.to_list()
    out_data=out_data[lt]
    # F_danon_phn(input_df,id='Unnamed: 0',pii_col='Phone Number')
    return out_data

def F_danon_ssn(df,id,pii_col):
    lst=[id,pii_col]
    df1=df[lst]
    print('Masking started for',pii_col,'.......')
    # Remove duplicates in-place
    df2=df1.drop_duplicates(subset=lst)
    df2.drop(pii_col,axis=1,inplace=True)

    lst_fk=[]
    for x in range(len(df2)):
        mask_data=fake.ssn()
        lst_fk.append(mask_data)
    df2[pii_col]=lst_fk
    #Merging with Original data
    input_data=df.drop(columns=[pii_col])
    out_data=input_data.merge(df2,how='left',on=id)
    print('Masking completed for',pii_col,'for ',len(lst_fk),' SSN')
    lt=df.columns.to_list()
    out_data=out_data[lt]
    # F_danon_ssn(input_df,id='Unnamed: 0',pii_col='SSN')
    return out_data
