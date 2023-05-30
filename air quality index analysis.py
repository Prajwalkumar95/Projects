# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 20:35:31 2022

@author: prajw
"""

import os
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
os.chdir("C:/Users/prajw/Downloads/python work")
dataset=pd.read_csv("data.csv",encoding='latin1')
dataset.tail(10)
dataset.shape
print(list(dataset.columns))
dataset.dtypes
DATA = dataset.info()
data = dataset.describe()
#checking if there is missing values
dataset.isna().any()
#Total number of missing values in the particular column
dataset.isna().sum()
#number of unique values in the columns
dataset.nunique()
#pairplot
sns.pairplot(data=dataset)
#count of values present in state column
dataset['state'].value_counts()
#count of values present in type column
dataset['type'].value_counts()

dataset.state.bar()
plt.xlabel('state')
plt.ylabel('Frequencies')
plt.plot()

plt.figure(figsize=(30, 10))
plt.xticks(rotation=90)
sns.barplot(x='state',y='so2',data=dataset)
plt.rcParams['figure.figsize']=(30,10)

dataset[['so2','state']].groupby(["state"]).mean().sort_values(by='so2').plot.bar(color='blue')

dataset[['rspm','state']].groupby(["state"]).mean().plot.bar(color='black')
#droping unnessary columns
dataset.drop(['agency','stn_code','date','sampling_date','location_monitoring_station'],axis=1,inplace=True)

so2_missing=dataset[dataset['date'].isnull()]
#dataset['type']=dataset['type'].fillna(dataset['type'].mode([]))
dataset['type']=dataset['type'].fillna(dataset['type'].mode()[0])
# null values are replaced with zeros for the numerical data
dataset.fillna(0, inplace=True)


def cal_SOi(so2):
    si=0
    if (so2<=40):
     si= so2*(50/40)
    elif (so2>40 and so2<=80):
     si= 50+(so2-40)*(50/40)
    elif (so2>80 and so2<=380):
     si= 100+(so2-80)*(100/300)
    elif (so2>380 and so2<=800):
     si= 200+(so2-380)*(100/420)
    elif (so2>800 and so2<=1600):
     si= 300+(so2-800)*(100/800)
    elif (so2>1600):
     si= 400+(so2-1600)*(100/800)
    return si
dataset['SOi']=dataset['so2'].apply(cal_SOi)
mydata= dataset[['so2','SOi']]
mydata.head()

def cal_Noi(no2):
    ni=0
    if(no2<=40):
     ni= no2*50/40
    elif(no2>40 and no2<=80):
     ni= 50+(no2-40)*(50/40)
    elif(no2>80 and no2<=180):
     ni= 100+(no2-80)*(100/100)
    elif(no2>180 and no2<=280):
     ni= 200+(no2-180)*(100/100)
    elif(no2>280 and no2<=400):
     ni= 300+(no2-280)*(100/120)
    else:
     ni= 400+(no2-400)*(100/120)
    return ni
dataset['Noi']=dataset['no2'].apply(cal_Noi)
mydata= dataset[['no2','Noi']]
mydata.head()
# calculating the individ

def cal_RSPMI(rspm):
    rpi=0
    if(rpi<=30):
     rpi=rpi*50/30
    elif(rpi>30 and rpi<=60):
     rpi=50+(rpi-30)*50/30
    elif(rpi>60 and rpi<=90):
     rpi=100+(rpi-60)*100/30
    elif(rpi>90 and rpi<=120):
     rpi=200+(rpi-90)*100/30
    elif(rpi>120 and rpi<=250):
     rpi=300+(rpi-120)*(100/130)
    else:
     rpi=400+(rpi-250)*(100/130)
    return rpi
dataset['Rpi']=dataset['rspm'].apply(cal_RSPMI)
mydata= dataset[['rspm','Rpi']]
mydata.head()


def cal_SPMi(spm):
    spi=0
    if(spm<=50):
     spi=spm*50/50
    elif(spm>50 and spm<=100):
     spi=50+(spm-50)*(50/50)
    elif(spm>100 and spm<=250):
     spi= 100+(spm-100)*(100/150)
    elif(spm>250 and spm<=350):
     spi=200+(spm-250)*(100/100)
    elif(spm>350 and spm<=430):
     spi=300+(spm-350)*(100/80)
    else:
     spi=400+(spm-430)*(100/430)
    return spi
   
dataset['SPMi']=dataset['spm'].apply(cal_SPMi)
mydata= dataset[['spm','SPMi']]
mydata.head()
# calculating the individual pollutant index for spm(suspended particulate matter)
def cal_aqi(si,ni,rspmi,spmi):
    aqi=0
    if(si>ni and si>rspmi and si>spmi):
     aqi=si
    if(ni>si and ni>rspmi and ni>spmi):
     aqi=ni
    if(rspmi>si and rspmi>ni and rspmi>spmi):
     aqi=rspmi
    if(spmi>si and spmi>ni and spmi>rspmi):
     aqi=spmi
    return aqi

dataset['AQI']=dataset.apply(lambda x:cal_aqi(x['SOi'],x['Noi'],x['Rpi'],x['SPMi']),axis=1)
mydata= dataset[['state','SOi','Noi','Rpi','SPMi','AQI']]
mydata.head()
# Caluclating the Air Quality Index.
def AQI_Range(x):
    if x<=50:
        return "Good"
    elif x>50 and x<=100:
        return "Moderate"
    elif x>100 and x<=200:
        return "Poor"
    elif x>200 and x<=300:
        return "Unhealthy"
    elif x>300 and x<=400:
        return "Very unhealthy"
    elif x>400:
        return "Hazardous"

mydata['AQI_Range'] = dataset['AQI'] .apply(AQI_Range)
dataset.head(15)
