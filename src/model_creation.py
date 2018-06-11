from src.preprocessing import Preprocessing
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

##Preprocessing on Train data
training_instance = Preprocessing(csv_filepath='../data/dataset.csv')
training_instance.taregtVariableEncoder()
training_instance.isMaleLabelEncoder()
training_instance.scalling()

## Dropping redundant features
X_train = training_instance.dataframe.drop(axis=1, columns=['IsMale', 'abnormal', 'cpt', 'low', 'normal', 'rxnorm', 'tag_dm2'])
y_train = training_instance.dataframe['tag_dm2']

model = RandomForestClassifier(n_estimators= 100, oob_score=True, n_jobs=-1, random_state=50, max_features="auto", min_samples_leaf=50)

model.fit(X_train, y_train)


# Preprocessing on Test Data
test_instance = Preprocessing(csv_filepath='../data/Test_dataset.csv')
test_instance.isMaleLabelEncoder()
test_instance.scalling(istrain=False)

X_test = test_instance.dataframe.drop(axis=1, columns=['IsMale', 'abnormal', 'cpt', 'low', 'normal', 'rxnorm'])

out_prob_list = model.predict_proba(X_test)
print(out_prob_list)

df = pd.read_csv('../data/test_dataset.csv')

list2 = df['patient_id']
list = out_prob_list[:,1]
lis = np.stack((list2,list), axis=-1)
df2 = pd.DataFrame(lis, columns=['patient_id','dm2_prob'])
df2.to_csv("manan_dm2_solution.csv")