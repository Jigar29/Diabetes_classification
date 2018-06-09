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

#Getting data in the python list
list = fetchDataFromJSON('../data/train.txt')

##Creating the dataset dictionary
class DatasetDict:
    def __init__(self):
        self.age = []
        self.ismale = []
        self.icd = []
        self.cpt = []
        self.rxnorm = []
        self.high = self.low = self.normal = self.abnormal = 0
        self.tag_dm2 = 0
        return

    def calculateAge(self):
        for i in list:
           self.age.append(int(((today - datetime.datetime.strptime((i['bday']), '%Y-%m-%d')).days) / 365))
        return

    def classifymale(self):
        for i in list:
            self.ismale.append(i['is_male'])
        return

    def resourceClassification(self):
        i = []
        for feature in list:
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

    def createADict(self):
        self.dictionary = {'Age':self.age, 'IsMale':self.ismale, 'cpt': self.cpt, 'icd': self.icd, 'rxnorm':self.rxnorm }
        return

    def createCSV(self):
        self.calculateAge()
        self.classifymale()
        self.createADict()
        self.resourceClassification()
        pd.DataFrame.from_dict(instance.dictionary).to_csv('../data/dataset.csv')
        return

instance = DatasetDict()

instance.createCSV()