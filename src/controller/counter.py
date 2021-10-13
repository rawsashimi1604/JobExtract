import pandas as pd
import numpy as np
from models.keywordsLook import KeywordsLookModel
from models.keywords import KeywordsModel


class Counter:
    def __init__(self):
        pass

    def updateKeywordsDict(self, keywordsList, description, keywordsDict):
        description = description.split(" ")
        for word in description:
            if word in keywordsList:
                keywordsDict[word] = keywordsDict.get(word, 0) + 1
        return keywordsDict

    def getExportLocation(self, dataFilePath):
        myFile = dataFilePath.split("/")[-1]
        location = dataFilePath.split("/")[-3]
        myFile = myFile.replace(".csv", "")
        myFile += "_keywords.csv"
        myFile = location.upper() + "_" + myFile
        return f"../data/keywords/{myFile}"

    def cleanDataframe(self, dataFilePath):
        df = pd.read_csv(dataFilePath)
        keywordsLookModel = KeywordsLookModel()
        # Keywords to search
        keywordsList = keywordsLookModel.allKeywords
        keywordsDependence = keywordsLookModel.dependenceKeywords
        keywordsIndependence = keywordsLookModel.independenceKeywords

        descriptions = df['description']

        # list of words and their count
        keywordsDict = {k: 0 for k in keywordsList}
        for description in descriptions:
            keywordsDict = self.updateKeywordsDict(
                keywordsList, description, keywordsDict)

        npShape = np.zeros(shape=(len(keywordsList), 3))
        myOutputDf = pd.DataFrame(
            npShape, columns=["keyword", "count", "type_"], dtype=str)
        # Add object to dataframe
        count = 0
        for word in list(keywordsDict.keys()):
            if word in keywordsDependence:
                kwObject = KeywordsModel(
                    word, keywordsDict[word], "dependence")
            else:
                kwObject = KeywordsModel(
                    word, keywordsDict[word], "independence")

            self.saveKeywordObject(kwObject, myOutputDf, count)
            count += 1

        # clean dataframe
        for i in range(len(myOutputDf.index)):
            if myOutputDf["keyword"][i] == "0.0":
                myOutputDf.drop(i, axis=0, inplace=True)

        return myOutputDf

    def exportToCSV(self, dataFilePath):
        df = self.cleanDataframe(dataFilePath)
        myDirPath = self.getExportLocation(dataFilePath)
        df.to_csv(myDirPath, index=False)

    def saveKeywordObject(self, keywordObject, dataframe, index):
        keywordObject.updateValues()
        for i in range(len(keywordObject.parameters)):
            dataframe[keywordObject.parameters[i]
                      ][index] = keywordObject.objectValues[i]


if __name__ == "__main__":
    myCounter = Counter()
    myFile = r"../data/cleanedData/Singapore/All/2021_09_29_21_34_Sales_dataFile.csv"
    myCounter.exportToCSV(myFile)

