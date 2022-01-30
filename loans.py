import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


loans1=pd.read_csv("data/loans.csv")
print(loans1.head())


# 1. Make column headers are variable names instead of values
loans2 = loans1.melt(id_vars=["id","account_id","date","amount","payments"])
print(loans2.head())

# 2. Splitting colunms
status = loans2["variable"].str.split("_").str.get(1)
month = loans2["variable"].str.split("_").str.get(0)

#Add these two columns and drop the redundant variable column
loans3 = loans2.assign(month=month,status=status).drop("variable",axis="columns")

print(loans3.head())
# 3. Remove missing values
loans4=loans3[loans3.value=="X"]

# remove the useless column
loans4=loans4.drop(columns="value")
print(loans4.head())



#  4. Transforming data
# a. change data types
print(loans4.dtypes)
loans4["month"]=loans4.month.astype("int")
loans4["status"]=loans4.status.astype("category")
print(loans4.dtypes)


loans4.to_csv("loans_py.csv")
