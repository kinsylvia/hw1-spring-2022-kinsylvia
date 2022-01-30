library(tidyverse)
library(janitor)
library(readr)
library(tidyr)
library(dplyr)
library(ggplot2)

loans = read_csv("data/loans.csv")
head(loans)

# 1. Make column headers are variable names instead of values
loans1 = loans %>% pivot_longer(cols=c(-id,-account_id, -date, -amount, -payments), names_to ="info")
head(loans1)

# 2. Splitting colunms
loans2 = loans1 %>% separate(info, c("month","status"), sep="_")
head(loans2)

# 3. Remove missing values with subset
loans2$value[loans2$value!="X"]= NA
head(loans2)
loans3 = subset(loans2, !is.na(value))
head(loans3)
# remove the useless column
loans3=loans3[,-8]
head(loans3)

#  4. Transforming data
# a. change data types
loans3["status"]=as.factor(loans3$status)
loans3["month"]=as.integer(loans3$month)
head(loans3)

# b. Order by id. 
loans4 = arrange(loans3, id)
head(loans4)

write.csv(loans4,"loans_r.csv")
