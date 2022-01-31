import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


accounts=pd.read_csv("data/accounts.csv")
accounts=pd.DataFrame(accounts)
print(accounts.head())

## --------------- now we have 1. account_id, 2. open_date, 3. statement_frequency.
print(accounts.dtypes)



## --------------- 4. get district_name
districts=pd.read_csv("data/districts.csv")
print(districts.head())

# accounts left join with districts to get district_id
print('LEFT JOIN 1: \n')
join1=accounts.merge(districts,left_on="district_id", right_on="id",how='left')
print(join1.head())
join1=join1.drop(['id_y','region','population','num_cities','urban_ratio','avg_salary','entrepreneur_1000','municipality_info','commited_crimes'],axis=1)
# rename column
join1.rename(columns={'name':'district_name'},inplace=True)
join1.rename(columns={'id_x':'account_id'},inplace=True)
join1=join1.drop(['unemployment_rate'],axis=1)
print(join1.head())

## --------------- 5. num_customers
clients=pd.read_csv('data/clients.csv')
print(clients.head())
links=pd.read_csv('data/links.csv')
print(links.head())

join2=join1.merge(links,left_on='account_id',right_on='account_id',how='left')
print(join2.head())
#join2.to_csv("join2.csv")
size=join2.groupby('account_id',as_index=False).agg({'id':'count'}).rename(columns={'id': 'num_customers'})

print(size.head())

join3=join1.merge(size,left_on='account_id',right_on='account_id',how='left')
print(join3.head())
#join3.to_csv("join3.csv")


## --------------- 6. credit_cards
cards=pd.read_csv('data/cards.csv')
print(cards.head())
cards_links=links.merge(cards,left_on='id',right_on='link_id',how='left')
print(cards_links.head())

size_cards=cards_links.groupby('id_x',as_index=False).agg({'id_y':'count'}).rename(columns={'id_x':'link_id','id_y':'credit_cards'})
join_ccards=links.merge(size_cards,left_on='id',right_on='link_id',how='outer')
print(join_ccards)

# remove duplicates
join_ccards=join_ccards.drop_duplicates(['account_id'])


join4=join3.merge(join_ccards,left_on='account_id',right_on='account_id',how='left')
print(join4.head())
join4.to_csv('join4.csv')

join4=join4.drop(['id','client_id','type','link_id'],axis=1)
print(join4.head())

## ----------------- 7.loan, 8.loan_amount, 9.loan_payments, 10.loan_term, 11.loan_status
loans=pd.read_csv('loans_py.csv')
print(loans.head())
join5=join4.merge(loans,left_on='account_id',right_on='account_id',how='left')
#join5.to_csv("join5.csv")
join5['loan']=join5['id'].isna().map({True:"F",False:'T'})
print(join5.head())

# rename to get loan_amount, loan_payments, loan_term, loan_status
join5=join5.rename(columns={'amount':'loan_amount'})
join5=join5.rename(columns={'payments':'loan_payments'})
join5=join5.rename(columns={'month':'loan_term'})
join5=join5.rename(columns={'status':'loan_status'})

## ----------------- 12. loan_default
join5['loan_default']=np.nan
join5['loan_default'][(join5['loan_status'] == 'A')] ='F'
join5['loan_default'][(join5['loan_status'] == 'C')] ='F'
join5['loan_default'][(join5['loan_status'] == 'B')] ='T'
join5['loan_default'][(join5['loan_status'] == 'D')] ='T'

print(join5.head())

## ---------------- 13. max_withdrawal

transactions = pd.read_csv("data/transactions.csv")
print(transactions.head())
# select debit account
debit=transactions[transactions['type'] == 'debit']
print(debit.head())

# group by account_id, get max amount, and rename to max_withdrawal.
debit_max=debit.groupby('account_id').agg({'amount':'max'}).rename(columns={'amount':'max_withdrawal'})
print(debit_max.head())

# join with the original table
join6=join5.merge(debit_max,left_on='account_id',right_on='account_id',how='left')
print(join6.head())

## ---------------- 14. min_withdrawal

# group by account_id, get min amount, and rename to min_withdrawal.
debit_min=debit.groupby('account_id').agg({'amount':'min'}).rename(columns={'amount':'min_withdrawal'})
print(debit_min.head())

# join with the original table
join7=join6.merge(debit_min,left_on='account_id',right_on='account_id',how='left')
print(join7.head())

#----------------- 15. cc_payments

credit=transactions[transactions['type'] == 'credit']
print(credit.head())
cc_payments=credit.groupby('account_id').size().reset_index(name='cc_payments')
print(cc_payments.head())

# join with the original table
join8=join7.merge(cc_payments,left_on='account_id',right_on='account_id',how='left')
print(join8.head())

#----------------- 16. max_balance
max_balance=transactions.groupby('account_id').agg({'balance':'max'}).rename(columns={'balance':'max_balance'})
print(max_balance.head())
# join with the original table
join9=join8.merge(max_balance,left_on='account_id',right_on='account_id',how='left')
print(join9.head())

#----------------- 17. min_balance
min_balance=transactions.groupby('account_id').agg({'balance':'min'}).rename(columns={'balance':'min_balance'})
print(min_balance.head())

# join with the original table
join10=join9.merge(min_balance,left_on='account_id',right_on='account_id',how='left')
print(join10.head())
join10=join10.rename(columns={'date_x':"open_date"})
join10=join10.drop(['district_id','Unnamed: 0','id','date_y'],axis=1)

join10.to_csv("analytical_py.csv")

