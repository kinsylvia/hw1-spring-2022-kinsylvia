library(tidyverse)
library(janitor)
library(readr)
library(tidyr)
library(dplyr)
library(ggplot2)

districts = read_csv("data/districts.csv")
head(districts)
dim(districts)
# Split colunms
districts1 = districts %>% separate(municipality_info, c("< 500","500-1999","2000-9999",">= 10000"), sep=",")
head(districts1)
districts1$`< 500`=substr(districts1$`< 500`,2,5)
districts1$`>= 10000`=substr(districts1$`>= 10000`,0,1)
head(districts1)

districts2 = districts1 %>% separate(unemployment_rate, c("unemployment_rate_95","unemployment_rate_96"), sep=",")
head(districts2)
districts2$`unemployment_rate_95`=substring(districts2$`unemployment_rate_95`,2)
districts2$`unemployment_rate_96`=substr(districts2$`unemployment_rate_96`,1,nchar(districts2$`unemployment_rate_96`)-1)
head(districts2)

districts3 = districts2 %>% separate(commited_crimes, c("crime_rate_95","crime_rate_96"), sep=",")
head(districts3)
districts3$`crime_rate_95`=substring(districts3$`crime_rate_95`,2)
districts3$`crime_rate_96`=substr(districts3$`crime_rate_96`,1,nchar(districts3$`crime_rate_96`)-1)
head(districts3)
dim(districts3)

write.csv(districts3,"district_r.csv")

#Each observation contains information including  uniquie district identifier, the district name, its region name, the number of inhabitants in this district,
# the number of cities of this district, its ratio of urban population, the average salary of population, the number of entrepreneurs per 1,000 inhabitants, 
# the number of municipalities with population <500, 500-1999, 2000-9999, and >= 10000, the unemployment rate and commited crime rate of this district in 95 and 96 respectively.
