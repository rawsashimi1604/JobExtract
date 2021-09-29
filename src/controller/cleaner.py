import nltk
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path


class Cleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.stem_words = SnowballStemmer("english")

    @staticmethod
    def downloadNLTK():
        # Run this function to download all NLTK libraries before using Cleaner
        nltk.download()

    def openData(self, filePath):
        # returns raw data dataframe for cleaning
        return pd.read_csv(filePath)

    def setCleanedDataFileDirectory(self, filePath):
        # create directory for cleaned data files
        return filePath.replace("rawData", "cleanedData")

    def makeCleanedDataFileDirectory(self, cleanDataFilePath):
        # create directory for cleaned data files, returns new directory and file name
        directoryPath = cleanDataFilePath.replace(
            "rawData", "cleanedData").split("/")[:-1]
        newPath = "/".join(directoryPath)

        path = Path(newPath)
        path.mkdir(parents=True, exist_ok=True)

        oldFileName = cleanDataFilePath.split("/")[-1]

        return f"{newPath}/{oldFileName}"

    def saveCleanedData(self, cleanedDataFrame, prevFilePath):
        filePath = self.makeCleanedDataFileDirectory(prevFilePath)
        # save the cleaned dataframe
        cleanedDataFrame.to_csv(filePath, index=False)

    def cleanFile(self, inputDataframe):
        # clean the dataframe
        df = inputDataframe
        df_len = len(df.index)
        for i in range(df_len):
            currDescription = df["description"][i]
            newDescription = self.cleanDescription(currDescription)
            df["description"][i] = newDescription

        return df

    def cleanDescription(self, descriptionString):
        # clean the description
        filtered_words = []

        stem_the_desc = self.stem_words.stem(descriptionString)
        descriptionString = stem_the_desc
        list_of_desc = word_tokenize(descriptionString)

        for w in list_of_desc:
            if w.isalnum():
                if w not in self.stop_words:
                    filtered_words.append(w)

        filtered_data_to_go_back_into_df = " ".join(
            map(str, filtered_words)).replace(",", "")

        descriptionString = filtered_data_to_go_back_into_df
        return descriptionString


if __name__ == "__main__":
    myCleaner = Cleaner()
    myDataFile = "../models/rawData/Singapore/All/2021_09_29_21_34_Sales_dataFile.csv"
    myData = myCleaner.openData(myDataFile)
    myCleanedData = myCleaner.cleanFile(myData)
    myCleaner.saveCleanedData(myCleanedData, myDataFile)
