import pandas as pd
import datetime as date
from sklearn.preprocessing import MinMaxScaler

dataframe = pd.read_csv("../data/dataset.csv")

for entry in range(0, len(dataframe['tag_dm2'])):
    if(dataframe['tag_dm2'][entry] != '0'):
        datetime_entry = date.datetime.strptime(dataframe['tag_dm2'][entry], '%Y-%m-%d')
        if(datetime_entry < date.datetime(year=2017, month=1, day= 1)):
            a =1
        elif((datetime_entry>= date.datetime(year=2017, month=1, day= 1)) and (datetime_entry <= date.datetime(year=2017, month=12, day= 31))):
           dataframe['tag_dm2'][entry] = 1
        else:
            dataframe['tag_dm2'][entry] = 0

print(dataframe['tag_dm2'])

