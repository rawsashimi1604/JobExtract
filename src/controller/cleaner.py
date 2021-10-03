from os import stat
import nltk
from nltk.grammar import cfg_demo
from nltk.util import pr
import pandas as pd
from langdetect import detect
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path
from jobs import JobsModel
import re
from datetime import datetime


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

    @staticmethod
    def saveJobObject(jobObject, dataframe, index):
        '''
            Updates the Job Object, saves to dataframe index.
        '''
        jobObject.updateValues()
        for i in range(len(jobObject.parameters)):
            dataframe[jobObject.parameters[i]
                      ][index] = jobObject.objectValues[i]
            print(jobObject)

    def cleanFile(self, inputDataframe):
        # clean the dataframe
        df = inputDataframe
        df_len = len(df.index)
        for i in range(df_len):
            # Initalize Job Object
            jobObject = JobsModel(
                df["jobTitle"][i],
                df["companyName"][i],
                df["location"][i],
                df["datePosted"][i],
                df["appStatus"][i],
                df["description"][i],
                df["seniorityLevel"][i],
                df["employmentType"][i],
                df["jobFunction"][i],
                df["industries"][i]
            )

            currDescription = jobObject.description
            newDescription = self.cleanDescription(currDescription)

            # If current language is not english, drop it from dataframe. Loop until found an english job description.
            if self.languageDetect(newDescription) != "en":
                df.drop(i, axis=0, inplace=True)

            else:
                # Set cleaned description if current language is english.
                jobObject.description = newDescription
                self.saveJobObject(jobObject, df, i)
            
        crawl_date = self.getCrawlDate(df)
        self.cleanPostedDate(df,crawl_date)

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

    def languageDetect(self, detectlanguage):
        english_or_not = detect(detectlanguage)
        return english_or_not

    def getCrawlDate(self,df):
        filename = re.search('([^/]*)$',df.attrs['filename']).group()
        return re.search('^\d{4}_\d{2}_\d{2}',filename).group()

    def cleanPostedDate(self, df, date):
        posted_timeframe = df['datePosted']
        posted_datelist = []
        crawl_date = datetime.strptime(date, "%Y_%m_%d")
        for item in posted_timeframe:
            posted_date = ""
            if not pd.isna(item):
                if re.search('day', item):
                    posted_date = crawl_date-pd.DateOffset(days=int(item[0]))
                elif re.search('week', item):
                    posted_date = crawl_date-pd.DateOffset(weeks=int(item[0]))
                elif re.search('month',item): 
                    posted_date = crawl_date-pd.DateOffset(months=int(item[0]))
                elif re.search('year',item):
                    posted_date = crawl_date-pd.DateOffset(years=int(item[0]))
            posted_datelist.append(str(posted_date)[0:10])
        df['datePosted'] = posted_datelist

if __name__ == "__main__":
    myCleaner = Cleaner()
    myDataFile = r"../data/rawData/Singapore/All/2021_09_29_21_34_Sales_dataFile.csv"
    myData = myCleaner.openData(myDataFile)
    myData.attrs['filename']= myDataFile # Set the 'filename' attribute to be the filepath to extract crawl date later
    myCleanedData = myCleaner.cleanFile(myData)
    myCleaner.saveCleanedData(myCleanedData, myDataFile)
