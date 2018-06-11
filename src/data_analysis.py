from src.preprocessing import Preprocessing

import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

##Preprocessing on Train data
training_instance = Preprocessing(csv_filepath='../data/dataset.csv', istrain= True)
training_instance.taregtVariableEncoder()
training_instance.isMaleLabelEncoder()
training_instance.scalling(istrain=True)

df1 = training_instance.dataframe

#Finding the correlation of the dataset
print(df1.corr())

#Scatter Plot
scatter_matrix(df1)
plt.show()