import pandas as pd
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

    def exportToCSV(self, dataFilePath):
        df = pd.read_csv(dataFilePath)
        descriptions = df['description']

        keywordsModel = KeywordsModel()
        keywordsList = keywordsModel.allKeywords
        keywordsDict = {k: 0 for k in keywordsList}
        for description in descriptions:
            keywordsDict = self.updateKeywordsDict(
                keywordsList, description, keywordsDict)

        # Create pandas series using dictionary, convert to dataframe
        keywordsSeries = pd.Series(data=keywordsDict)
        keywordsDf = keywordsSeries.to_frame()

        # Create columns
        keywordsDf['keywords'] = keywordsDf.index
        keywordsDf.rename({0: "count"}, axis=1, inplace=True)

        # Rearrange columns
        keywordsDf = keywordsDf[["keywords", "count"]]

        # Export to directory path
        myDirPath = self.getExportLocation(dataFilePath)
        keywordsDf.to_csv(myDirPath, index=False)


if __name__ == "__main__":
    myCounter = Counter()
    myFile = r"../data/cleanedData/Singapore/All/2021_09_29_21_34_Sales_dataFile.csv"
    myCounter.exportToCSV(myFile)

# keywords_singapore
# keywords_usa
# keywords_russia
# keywords_china

# Singapore Excel file
