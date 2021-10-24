from __future__ import annotations
from os import stat
import langdetect
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

"""
    Cleaner Module. Contains Cleaner Object, used for cleaning rawData files and export to cleanedData folder.
"""

class Cleaner:
    '''
        Cleaner object, used for cleaning rawData files and export to cleanedData folder.

        Class Attributes:
            None
    '''
    def __init__(self) -> Cleaner:
        '''
            Constructor for Cleaner Class.
            Parameters:
                None
            Returns:
                Cleaner => Constructs Cleaner Class
        '''
        self.stop_words = set(stopwords.words("english"))
        self.stem_words = SnowballStemmer("english")
        self.fileLocation = ""

    @staticmethod
    def downloadNLTK() -> None:
        '''
            Downloads all NLTK required data
            Parameters:
                None
            Returns:
                None
        '''
        # Run this function to download all NLTK libraries before using Cleaner
        nltk.download()

    def startCleaner(self, myDataFile: str) -> None:
        '''
            Main cleaner function to clean files and save to new CSV
            Parameters:
                myDataFile : str => rawData file to clean
            Returns:
                None
        '''
        myData = self.openData(myDataFile)
        self.fileLocation = myDataFile
        # Set the 'filename' attribute to be the filepath to extract crawl date later
        myData.attrs['filename'] = myDataFile
        myCleanedData = self.cleanFile(myData)
        self.saveCleanedData(myCleanedData, myDataFile)

    def openData(self, filePath: str) -> pd.DataFrame:
        '''
            Creates dataframe from CSV file
            Parameters:
                filePath : str => rawData CSV file to clean
            Returns:
                pd.DataFrame => Dataframe with CSV intialized
        '''
        # returns raw data dataframe for cleaning
        return pd.read_csv(filePath)

    def makeCleanedDataFileDirectory(self, rawDataFilePath: str) -> str:
        '''
            Creates file directory to store cleaned file in if it does not exist
            Parameters:
                rawDataFilePath : str => rawData file path to clean
            Returns:
                str => File Directory to store cleaned file in
        '''
        directoryPath = rawDataFilePath.replace(
            "rawData", "cleanedData").split("/")[:-1]
        newPath = "/".join(directoryPath)

        path = Path(newPath)
        path.mkdir(parents=True, exist_ok=True)

        oldFileName = rawDataFilePath.split("/")[-1]

        return f"{newPath}/{oldFileName}"

    def saveCleanedData(self, cleanedDataFrame: pd.DataFrame, rawDataFilePath: str) -> None:
        '''
            Saves cleaned dataframe to CSV file in specified directory
            Parameters:
                cleanedDataFrame : pd.DataFrame => Cleaned Dataframe to create CSV file with
                rawDataFilePath : str => rawData file path to clean
            Returns:
                None
        '''
        filePath = self.makeCleanedDataFileDirectory(rawDataFilePath)
        cleanedDataFrame.to_csv(filePath, index=False)

    @staticmethod
    def saveJobObject(jobObject: JobsModel, dataframe: pd.DataFrame, index: int) -> None:
        '''
            Save job object to dataframe's specific index
            Parameters:
                jobObject : JobsModel => JobsModel object to save to dataframe
                dataframe : pd.DataFrame => Dataframe to save to
                index : int => Index location to store keywordObject in

            Returns:
                None
        '''
        jobObject.updateValues()
        for i in range(len(jobObject.parameters)):
            dataframe[jobObject.parameters[i]
                      ][index] = jobObject.objectValues[i]

    def cleanFile(self, inputDataframe: pd.DataFrame) -> pd.DataFrame:
        '''
            Cleans rawData file, removing non english rows, removing non date rows, creating date data, creating applicants data, settings location data.
            Parameters:
                inputDataframe : pd.DataFrame => rawData DataFrame

            Returns:
                None
        '''
        df = inputDataframe
        df_len = len(df.index)
        
        # Get current job position file selected
        currPositionDict = dict(df["seniorityLevel"].value_counts()[:5])
        # If it is not "All" File
        if len(currPositionDict) == 1:
            changePositionFlag = True
        else:
            changePositionFlag = False

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
            if not self.languageDetect(newDescription):
                df.drop(i, axis=0, inplace=True)
            
            # If date posted is empty
            elif type(jobObject.datePosted) == float:
                df.drop(i, axis=0, inplace=True)

            else:
                # Set cleaned description if current language is english.
                jobObject.description = newDescription

                # Get new date if date exists, set cleaned date if date exists.
                crawlDate = self.getCrawlDate(df)
                cleanedDate = self.getPostedDate(crawlDate, jobObject.datePosted)
                jobObject.datePosted = cleanedDate

                cleanedAppStatus = self.cleanAppStatus(jobObject.appStatus)
                jobObject.appStatus = cleanedAppStatus

                # Set seniorityLevel if field is empty and file is not "ALL"
                if changePositionFlag:
                    jobObject.seniorityLevel = list(currPositionDict.keys())[0]
                
                jobObject.location = self.cleanLocation(self.fileLocation)
                # Save new object to dataframe
                self.saveJobObject(jobObject, df, i)

        return df

    def cleanDescription(self, descriptionString: str) -> str:
        '''
            Cleans description, remove stopwords, utilises stemming, removes punctuation.
            Parameters:
                descriptionString : str => rawData DataFrame

            Returns:
                str => Cleaned description
        '''
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

    def cleanLocation(self, filePath: str) -> str:
        '''
            Cleans location, setting location to filePath path folder name.
            Parameters:
                filePath : str => Directory to extract location from

            Returns:
                str => Location to set
        '''
        locations = ["Singapore", "Russia", "China", "USA"]
        for location in locations:
            if location in filePath:
                return location
    
        return ""

    def languageDetect(self, description: str) -> bool:
        '''
            Detects language 
            Parameters:
                description : str => Description to check language in

            Returns:
                bool => True if english, False if not
        '''
        try:
            english_or_not = detect(description)

        except langdetect.LangDetectException:
            return False

        return english_or_not == "en"

    def getCrawlDate(self, dataframe: pd.DataFrame) -> str:
        '''
            Gets date from dataframe attribute
            Parameters:
                dataframe : pd.DataFrame => Dataframe to search

            Returns:
                str => Date of Crawling
        '''
        filename = re.search('([^/]*)$', dataframe.attrs['filename']).group()
        return re.search('^\d{4}_\d{2}_\d{2}', filename).group()

    def getPostedDate(self, filenameDate: str, postedDate: str) -> str:
        '''
            Gets date of LinkedIn posting
            Parameters:
                filenameDate : str => Crawl Date
                postedDate : str => rawData Date Posted field

            Returns:
                str => Date of LinkedIn posting
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

    def cleanAppStatus(self, appStatus: str) -> str:
        '''
            Gets number of applicants in job posting
            Parameters:
                appStatus : str => appStatus data field in rawData

            Returns:
                str => Number of applicants in job posting
        '''
        pattern_string = "Be among the first 25 applicants"
        if appStatus == pattern_string:
            appStatus = "< 25 applicants"
        return appStatus

if __name__ == "__main__":
    myCleaner = Cleaner()
    myDataFile = r"../data/rawData/USA/Mid-Senior/2021_10_09_14_59_Sales_dataFile.csv"
    myCleaner.startCleaner(myDataFile)
