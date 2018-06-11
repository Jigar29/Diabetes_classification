import pandas as pd
import datetime as date
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

class Preprocessing():
    def __init__(self, csv_filepath):
        self.scaler = MinMaxScaler()
        self.labelencoder = LabelEncoder()
        self.dataframe = pd.read_csv(csv_filepath)
        return

    def taregtVariableEncoder(self):
        for entry in range(0, len(self.dataframe['tag_dm2'])):
            if (self.dataframe['tag_dm2'][entry] != '0'):
                datetime_entry = date.datetime.strptime(self.dataframe['tag_dm2'][entry], '%Y-%m-%d')
                if (datetime_entry < date.datetime(year=2017, month=1, day=1)):
                    self.dataframe['tag_dm2'][entry] = np.nan
                elif ((datetime_entry >= date.datetime(year=2017, month=1, day=1)) and (
                        datetime_entry <= date.datetime(year=2017, month=12, day=31))):
                    self.dataframe['tag_dm2'][entry] = 1
                else:
                    self.dataframe['tag_dm2'][entry] = 0

        self.dataframe = self.dataframe.dropna()
        return

    def isMaleLabelEncoder(self):
        self.dataframe['IsMale'] = self.labelencoder.fit_transform(self.dataframe['IsMale'])
        return

    def scalling(self , istrain = True):
        # Min-Max Scalling on the dataset
        if(istrain == True):
            self.dataframe = pd.DataFrame(self.scaler.fit_transform(self.dataframe), columns= ['Age', 'IsMale','abnormal', 'cpt', 'high', 'icd', 'low', 'normal', 'rxnorm', 'tag_dm2'])
        else:
            self.dataframe = self.dataframe.drop(axis= 1, columns=['patient_id'])
            self.dataframe = pd.DataFrame(self.scaler.fit_transform(self.dataframe),columns=['Age', 'IsMale', 'abnormal', 'cpt', 'high', 'icd', 'low', 'normal','rxnorm'])
        return