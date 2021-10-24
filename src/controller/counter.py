from __future__ import annotations
import pandas as pd
import numpy as np
from models.keywordsLook import KeywordsLookModel
from models.keywords import KeywordsModel

"""
    Counter Module. Contains Counter Object, used for counting keywords in data, and returning a CSV file containg keywords and count
"""

class Counter:
    '''
        Counter object, used for counting keywords in data, and returning a CSV file containg keywords and count

        Class Attributes:
            None
    '''
    def __init__(self) -> Counter:
        '''
            Constructor for Counter Class.
            Parameters:
                None
            Returns:
                Counter => Constructs Counter Class
        '''
        pass

    def updateKeywordsDict(self, keywordsList: list, description: str, keywordsDict: dict) -> dict:
        '''
            Updates dictionary that stores keywords and their count after passing in a description
            Parameters:
                keywordsList : list => List of all available keywords to search
                description : str => Description string to search keywords in
                keywordsDict : dict => Dictionary to update

            Returns:
                dict => Returns updated keywords dictionary
        '''
        description = description.split(" ")
        for word in description:
            if word in keywordsList:
                keywordsDict[word] = keywordsDict.get(word, 0) + 1
        return keywordsDict

    def getExportLocation(self, dataFilePath: str) -> str:
        '''
            Get export location and filename to save CSV file to.
            Parameters:
                dataFilePath : str => Data file path to search keywords in

            Returns:
                str => Directory and filename of CSV file
        '''
        myFile = dataFilePath.split("/")[-1]
        myFile = myFile.replace(".csv", "")
        myFile = "KEYWORDS" + "_" + myFile + ".csv"

        return f"../data/keywords/{myFile}"

    def cleanDataframe(self, dataFilePath: str) -> pd.DataFrame:
        '''
            Constructs dataframe to store CSV file in
            Parameters:
                dataFilePath : str => Data file path to search keywords in

            Returns:
                pd.DataFrame => Dataframe to store CSV file in
        '''
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
            elif word in keywordsIndependence:
                kwObject = KeywordsModel(
                    word, keywordsDict[word], "independence")

            self.saveKeywordObject(kwObject, myOutputDf, count)
            count += 1

        # clean dataframe
        for i in range(len(myOutputDf.index)):
            if myOutputDf["keyword"][i] == "0.0":
                myOutputDf.drop(i, axis=0, inplace=True)

        return myOutputDf

    def saveKeywordObject(self, keywordObject: KeywordsModel, dataframe: pd.DataFrame, index: int) -> None:
        '''
            Save keyword object to dataframe's specific index
            Parameters:
                keywordObject : KeywordsModel => keywordModel object to save to dataframe
                dataframe : pd.DataFrame => Dataframe to save to
                index : int => Index location to store keywordObject in

            Returns:
                None
        '''
        keywordObject.updateValues()
        for i in range(len(keywordObject.parameters)):
            dataframe[keywordObject.parameters[i]
                      ][index] = keywordObject.objectValues[i]

    def exportToCSV(self, dataFilePath) -> None:
        '''
            Main function to get keywords from
            Parameters:
                dataFilePath : str => Data file path to search keywords in

            Returns:
                None
        '''
        df = self.cleanDataframe(dataFilePath)
        myDirPath = self.getExportLocation(dataFilePath)
        df.to_csv(myDirPath, index=False)
    


if __name__ == "__main__":
    myCounter = Counter()
    myFile = r"../data/mergedData/AllCountries_All_Data.csv"
    myCounter.exportToCSV(myFile)

