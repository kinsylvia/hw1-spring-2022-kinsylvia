import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

districts=pd.read_csv("data/districts.csv")
print(districts.head())
print(districts.dtypes)
districts['municipality_info']=districts.municipality_info.astype('string')
districts['unemployment_rate']=districts.unemployment_rate.astype('string')
districts['commited_crimes']=districts.commited_crimes.astype('string')


# 1. Splitting municipality_info colunms
less_than_500 = districts["municipality_info"].str.split(",").str.get(0)
print(less_than_500.head())
less_than_500=less_than_500.str.lstrip("[")
print(less_than_500.head())

between_500_and_1999 = districts["municipality_info"].str.split(",").str.get(1)
print(between_500_and_1999.head())

between_2000_and_9999 = districts["municipality_info"].str.split(",").str.get(2)
print(between_2000_and_9999.head())


more_than_10000 = districts["municipality_info"].str.split(",").str.get(3)
print(more_than_10000.head())

# change the data type to string
more_than_10000=more_than_10000.astype('string')


more_than_10000=more_than_10000.str.split("").str.get(1)
print(more_than_10000.head())

districts1=districts.assign(less_than_500=less_than_500,between_500_and_1999=between_500_and_1999,between_2000_and_9999=between_2000_and_9999,more_than_10000=more_than_10000).drop("municipality_info",axis="columns")
print(districts1)

# 2. Splitting unemployment_rate colunms
print(districts1.unemployment_rate.head())
unemployment_rate_95 = districts1["unemployment_rate"].str.split(",").str.get(0)
print(unemployment_rate_95.head())

unemployment_rate_96 = districts1["unemployment_rate"].str.split(",").str.get(1)
print(unemployment_rate_96.head())


# remove special character
unemployment_rate_95=unemployment_rate_95.str.lstrip('[')
# change the data type to string
unemployment_rate_96=unemployment_rate_96.astype('object')
print(unemployment_rate_96)
unemployment_rate_96=unemployment_rate_96.str.split("]").str.get(0)
print(unemployment_rate_96.head())


#assign the new columns to original table
districts2=districts1.assign(unemployment_rate_95=unemployment_rate_95,unemployment_rate_96=unemployment_rate_96).drop("unemployment_rate",axis="columns")
print(districts2)


# 3. Splitting commited_crimes colunms
print(districts2.commited_crimes.head())
crime_rate_95 = districts2["commited_crimes"].str.split(",").str.get(0)
print(crime_rate_95.head())

crime_rate_96 = districts2["commited_crimes"].str.split(",").str.get(1)
print(crime_rate_96.head())


# remove special character
crime_rate_95=crime_rate_95.str.lstrip('[')
print(crime_rate_95.head())
# change the data type to string
crime_rate_96=crime_rate_96.astype('object')
print(crime_rate_96)
crime_rate_96=crime_rate_96.str.split("]").str.get(0)
print(crime_rate_96.head())


#assign the new columns to original table
districts3=districts2.assign(crime_rate_95=crime_rate_95,crime_rate_96=crime_rate_96).drop("commited_crimes",axis="columns")
print(districts3)

districts3.to_csv("district_py.csv")

