"""

Author: Amogh Jalihal

Date: 2015/11/16

Script to read csv files specific to TAGs and plotting bar plots
and pie chart to summarize work done in the last one week.
Needs output from 

"""
print("Starting python script...")

import pandas as pd
import os 
import re
import matplotlib.pyplot as plt
import datetime
import numpy as np

####################################################################
"""
Specify figure dimensions here
"""
plt.rcParams['figure.figsize'] = 5, 10

HOME=os.path.expanduser("~")

"""
Customize this path
"""
REPORTS_PATH="/orgs/reports/"

"""
Initialize variables
"""

Day_Of_Week=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

CLOCKDICT={}

"""
Read tags from tags.txt
These do not have necessarily have to be actual tags,
just meaningful desciptions used in the #+NAME field
"""
TAGS=[]
with open(HOME+REPORTS_PATH+"tags.txt",'r') as listoftags:
    for line in listoftags.readlines():
        TAGS.append(line.split('\n')[0])
for d in Day_Of_Week:
    CLOCKDICT[d]={}
    for t in TAGS:
        CLOCKDICT[d][t]=0

labels_list=[]
cum_hours=[]

f,(ax1,ax2)=plt.subplots(2,1)
####################################################################
print("Reading tags...")

"""
Read each csv file and store them as dictionary. 
Each day of the week has this dictionary of associated values.
"""
for tag in TAGS:
    df=pd.read_csv(HOME+REPORTS_PATH+"csv/"+tag+".csv",sep=",")
    for day_in_week in Day_Of_Week:
        if not df[df['Headline'].str.contains(day_in_week)].empty:
            t=df[df['Headline'].str.contains(day_in_week)]._values[0][4]
            time=t.split(":")
            totaltime=float(time[0])+float(time[1])/60.0
            CLOCKDICT[day_in_week][tag]=totaltime

"""
Convert dictionary to dataframe and reindex to sort days of the week
"""

FinalTimes=pd.DataFrame.from_dict(CLOCKDICT)
FT=FinalTimes.transpose().reindex(Day_Of_Week)

"""
Don't plot empty hours
"""

for c in FT.columns:
    dropflag = False
    if sum(FT[c]) == 0:
        FT = FT.drop([c], axis=1)

print(FT)

print("Plotting...")
"""
Plot bar graph of day wise split up
"""
FT.plot.bar(rot='45',ax=ax1)
ax1.set_ylabel('Hours')


for c in FT.columns:
    cum_hours.append(FT[c].sum())
    labels_list.append(c)

def absolute_value(val):
    """
    This function is required to display absolute values
    Source: https://stackoverflow.com/a/41089685
    """
    a  = np.round(val/100.*np.array(cum_hours).sum(), 0)
    return a

"""
Plot pie chart of cumulative hours spent on each TAG
"""
ax2.pie(cum_hours,labels=labels_list,autopct=absolute_value)
ax2.set_title('Total time clocked this week = '+str(sum(cum_hours)),position=(0.5,-0.1))
ax2.axis('equal')


today=datetime.datetime.now()
year=str(today.year)
month=str(today.month)
day=today.day
week=''
if day<8:
    week='1'
elif day>7 and day<15:
    week='2'
elif day>14 and day<22:
    week='3'
elif day>21 and day < 28:
    week='4'
else:
    week='5'
print("Saving report...")
plt.savefig(HOME+REPORTS_PATH+year+"-"+month+"-w"+week+"-report.png",bbox='tight')

print("All done!")
