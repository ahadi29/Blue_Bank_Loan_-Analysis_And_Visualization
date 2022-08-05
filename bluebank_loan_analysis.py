# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:04:54 2022

@author: ahadi
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Method 1 to read json dataset
json_file = open('loan_data_json.json') #Open the json file
data=json.load(json_file)               #Load the json file

#Method 2 to read json dataset
with open('loan_data_json.json') as json_file:
    data = json.load(json_file)
   
#Transforming to dataframe

loandata = pd.DataFrame(data)

#Finding unique values for the purpose column
loandata['purpose'].unique()

#Describing the data
loandata.describe()

#Describing the data of a specific column
loandata['int.rate'].describe()
loandata['fico'].describe()

#Describing the data of debt to income ratio(dti)
loandata['dti'].describe()

#Log Annual Income field in the dataset - It means the annual income in our data set is in the form of log i.e. we have to take the exponent of it to get the actual value.
#Using numpy we will take the exponent of the log annual income field to get the actual income value. 

#Using EXP() to get the annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annual.income'] = income



## Fico Score:
# fico >= 300 and < 400: 'Very Poor'
# fico >= 400 and ficoscore < 600: 'Poor'
# fico >= 601 and ficoscore < 660: 'Fair'
# fico >= 660 and ficoscore < 780: 'Good'
# fico >= 780: 'Excellent'

## To see only one value of a column from our dataset. loandata['fico'][0] ## Type this in console. This retrives the fico columns index 0.

#Applying loops on fico values
#Retrieving max number of rows
length = len(loandata)
ficocat=[]
for x in range(0,length):
    fico = loandata['fico'][x]
    try:
        if fico >= 300 and fico < 400:
            cat = 'Very Poor'
        elif fico >= 400 and fico < 600:
            cat = 'Poor' 
        elif fico >= 601 and fico < 660:
            cat = 'Fair'
        elif fico >= 660 and fico < 700:
            cat = 'Good'
        elif fico>=700:
            cat = 'Excellent'
        else:
            ficocat = 'Unknown'
    except:
        ficocat = 'Unknown'
    ficocat.append(cat)

#Telling python to convert ficocat into series
#As ficocat is in the format of list and series is column in dataframe.
ficocat = pd.Series(ficocat)


# Adding the ficocat to our dataframe
loandata['fico.category'] = ficocat


#df.loc as conditional statement
# df.loc[df[columnname] condition, newcolumnname] = 'value if the condition is met'

#for interest rates, a new column is wanted. If the rate>0.12 then high else low.

loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type' ] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

#Number of loans/rows by fico category
#Size represents number of rows.

catplot = loandata.groupby(['fico.category']).size()  #This line count the number of rows per category and groups it together.
catplot.plot.bar(color='yellow', width=0.2)
plt.show()

purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color='red', width=0.1)
plt.show()


#Scatter plots

xpoint = loandata['dti']
ypoint = loandata['annual.income']
plt.scatter(xpoint,ypoint, color='#4caf50')
plt.show()


#Writing to csv with an index(To uniquely identify rows)

loandata.to_csv('loandata_cleaned.csv',index = True)