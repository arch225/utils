from flask import render_template, request,Flask,jsonify
from flask_cors import CORS
import pandas as pd
from faker import Faker
import os

fake=Faker()

app = Flask(__name__)

#This part of code is not required, is created for testing purpose

def fak_dat_gen(n):
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

sher=pd.read_csv('fake_data.csv')
x={
    'column_name':list(sher.columns),
    'PII_indicator':[0,0,1,1,0,0,0],
    'PII_type':['','','pii-email','pii-ssn','','',''],
    'Anon_method':['','','mask','fk-ssn','','','']
}
print(pd.DataFrame(x))

#End of testing

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/getdata', methods=['POST'])
def upload_file():
    global sher
    file = request.files['file']
    if file:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension in ['.xlsx', '.xls', '.csv']:
            try:
                if file_extension in ['.xlsx', '.xls']:
                    sher = pd.read_excel(file)
                else:
                    sher = pd.read_csv(file)
                return sher.to_json(orient='records')
            except Exception as e:
                return str(e), 400
        else:
            return 'Invalid file format. Only Excel and CSV files are supported.', 400
    else:
        return 'No file uploaded.', 400

@app.route('/getmeta',methods=['GET'])
def get_meta():
    global sher
    return jsonify(list(sher.columns))

@app.route('/getconfig', methods=['POST'])
def get_config():
    data=request.get_json()
    df=pd.DataFrame(data)
    df.to_csv('config.csv', index=False)
    return 'Lodu Lalit'

@app.route('/anonymize', methods=['GET'])
def anonymize():
    global x
    config_pd=pd.DataFrame(x)
    config_pd1=config_pd[config_pd['PII_indicator']==1]
    sher_out=sher
    for i in range(len(config_pd1)):
        print(config_pd1.iloc[i,0],config_pd1.iloc[i,2],config_pd1.iloc[i,3])
        if config_pd1.iloc[i,2]=='pii-email':
            print('Anonymizing: ',config_pd1.iloc[i,0])
            sher_out=F_danon_email(sher_out, id='ID', pii_col=config_pd1.iloc[i, 0])
            print('Anonymization of ',config_pd1.iloc[i,0],' is completed')
        elif config_pd1.iloc[i,2]=='pii-ssn':
            print('Anonymizing: ',config_pd1.iloc[i,0])
            sher_out=F_danon_ssn(sher_out, id='ID', pii_col=config_pd1.iloc[i, 0])
            print('Anonymization of ',config_pd1.iloc[i,0],' is completed')
    sher_out.to_csv('fake_out.csv', index=False)
    return jsonify(sher_out.to_json(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
