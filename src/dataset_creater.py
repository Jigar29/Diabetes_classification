import json
import pandas as pd
import datetime

##Today's Date
today = datetime.datetime(year=2016, month=12, day= 31)

##Fetching the data from the JSON training file
def fetchDataFromJSON(filepath):
    ls = []
    with open(filepath) as f:
        for line in f:
            ls.append(json.loads(line))
    return ls

##Creating the dataset dictionary
class DatasetDict:
    def __init__(self, filepath):
        self.age = []
        self.ismale = []
        self.icd = []
        self.cpt = []
        self.rxnorm = []
        self.high = []
        self.low = []
        self.normal = []
        self.abnormal = []
        self.tag_dm2 = []
        self.list = fetchDataFromJSON(filepath)
        return

    def calculateAge(self):
        for i in self.list:
           self.age.append(int(((today - datetime.datetime.strptime((i['bday']), '%Y-%m-%d')).days) / 365))
        return

    def classifymale(self):
        for i in self.list:
            self.ismale.append(i['is_male'])
        return

    def resourceClassification(self):
        i = []
        for feature in self.list:
            cpt = 0
            icd = 0
            rxnorm = 0
            for resource in feature['resources']:
                for item in feature['resources'][resource]:
                    if(item[0:3] == 'cpt'):
                        cpt = cpt + 1
                    elif (item[0:3] == 'icd'):
                        icd = icd + 1
                    elif (item[0:5] == 'rxnorm'):  #tobefixed
                        rxnorm = rxnorm + 1

            self.cpt.append(cpt)
            self.icd.append(icd)
            self.rxnorm.append(rxnorm)
        return

    def observaionClassification(self):
        for feature in self.list:
            high = normal = low = abnormal = 0
            for observation in feature['observations']:
                for dictionary in feature['observations'][observation]:
                    if(dictionary['interpretation'] == 'H'):
                        high = high + 1
                    elif(dictionary['interpretation'] == 'L'):
                        low = low + 1
                    elif(dictionary['interpretation'] == 'A'):
                        abnormal = abnormal + 1
                    elif(dictionary['interpretation'] == 'N'):
                        normal = normal + 1
            self.high.append(high)
            self.low.append(low)
            self.abnormal.append(abnormal)
            self.normal.append(normal)
        return

    def targetVariable(self):
        for feature in self.list:
            if(feature['tag_dm2'] == ''):
                self.tag_dm2.append(0)
            else:
                self.tag_dm2.append(feature['tag_dm2'])
        return

    def createADict(self, is_train):
        if(is_train == True):
            self.dictionary = {'Age':self.age, 'IsMale':self.ismale, 'cpt': self.cpt, 'icd': self.icd, 'rxnorm':self.rxnorm, 'high': self.high, 'low':self.low, 'normal':self.normal, 'abnormal':self.abnormal, 'tag_dm2': self.tag_dm2}
        else:
            self.dictionary = {'Age': self.age, 'IsMale': self.ismale, 'cpt': self.cpt, 'icd': self.icd,
                               'rxnorm': self.rxnorm, 'high': self.high, 'low': self.low, 'normal': self.normal,
                               'abnormal': self.abnormal}
        return

    def createCSV(self, is_train= True, data_set_name= None):
        self.calculateAge()
        self.classifymale()
        self.resourceClassification()
        self.observaionClassification()
        if(is_train == True):
            self.targetVariable()
        self.createADict(is_train)
        pd.DataFrame.from_dict(self.dictionary).to_csv('../data/' +data_set_name+ '.csv')
        return

#Creating the training dataset
training_instance = DatasetDict('../data/train.txt')
training_instance.createCSV(is_train= True, data_set_name= 'dataset')

#Creating the test Dataset
test_instance = DatasetDict('../data/test.txt')
test_instance.createCSV(is_train=False, data_set_name='Test_dataset')