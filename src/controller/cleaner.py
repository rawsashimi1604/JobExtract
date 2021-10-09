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
from models.jobs import JobsModel
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

    def cleanFile(self, inputDataframe):
        # clean the dataframe
        df = inputDataframe
        df_len = len(df.index)

        # Clean each row, update jobObject, then set jobObject values to csv
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

                # Get new date if date exists, set cleaned date if date exists.
                crawlDate = self.getCrawlDate(df)
                cleanedDate = self.getPostedDate(
                    crawlDate, jobObject.datePosted)
                jobObject.datePosted = cleanedDate

                # Save new object to dataframe
                self.saveJobObject(jobObject, df, i)

        return df

    def cleanDescription(self, descriptionString):
        # clean the description
        filtered_words = []
        descriptionString = str(descriptionString)
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

    def getCrawlDate(self, dataframe):
        '''
            Get date from CSV filename
        '''
        filename = re.search('([^/]*)$', dataframe.attrs['filename']).group()
        return re.search('^\d{4}_\d{2}_\d{2}', filename).group()

    def getPostedDate(self, filenameDate, postedDate):
        ''' 
            Get date of job posting using filename and raw posted date
        '''
        crawl_date = datetime.strptime(filenameDate, "%Y_%m_%d")
        posted_date = ""
        if not pd.isna(postedDate):
            if re.search('day', postedDate):
                posted_date = crawl_date-pd.DateOffset(days=int(postedDate[0]))
            elif re.search('week', postedDate):
                posted_date = crawl_date - \
                    pd.DateOffset(weeks=int(postedDate[0]))
            elif re.search('month', postedDate):
                posted_date = crawl_date - \
                    pd.DateOffset(months=int(postedDate[0]))
            elif re.search('year', postedDate):
                posted_date = crawl_date - \
                    pd.DateOffset(years=int(postedDate[0]))

        return str(posted_date)[0:10]


if __name__ == "__main__":
    myCleaner = Cleaner()
    myDataFile = r"../data/rawData/Russia/Director/2021_10_08_23_43_Sales_dataFile.csv"
    myData = myCleaner.openData(myDataFile)
    # Set the 'filename' attribute to be the filepath to extract crawl date later
    myData.attrs['filename'] = myDataFile
    myCleanedData = myCleaner.cleanFile(myData)
    myCleaner.saveCleanedData(myCleanedData, myDataFile)
