from __future__ import annotations
from typing import Optional
from cleaner import Cleaner
from merger import Merger
from augmentor import Augmentor
from datetime import datetime
import os

"""
    Processor Module. Contains Processor Object, used for processing raw data into processed data.
"""


class Processor:
    """
        Processor Object, used for processing raw data into processed data.
    """
    def __init__(self, format: str, manualFilePath: Optional[str]=None) -> Processor:
        '''
            Constructor for Processor Class.
            Parameters:
                format: str => Defines which files are to be processed.
                Available Parameters:
                    "all" => Processes all files in all rawData directories,
                    "latestAll" => Processes latest files in all rawData directories
                    "single" => Processes single file, manualFilePath attribute needed
                manualFilePath: str (Optional) => Specifies path for "single" format processing.
            Returns:
                Processor => Constructs Processor Class
        '''

        # List of files to process
        self.files = []
        self.mergedFilePath = ""

        self.format = format
        self.manualFilePath = manualFilePath

    @staticmethod
    def dateTime() -> str:
        '''
            Returns today's date and time
            Parameters:
                None
            Returns:
                str => Formatted string containing date and time.
        '''
        now = datetime.now()
        datetime_string = now.strftime("%Y_%m_%d_%H_%M")

        return datetime_string

    def cleanFiles(self) -> None:
        '''
            Cleans all files according to specified format attribute, adds cleaned files into class attributes to be accessed by other functions.
            Parameters:
                None
            Returns:
                None
        '''
        formatOptions = ["single", "all", "latestAll"]
        print(f"Format selected is {self.format}. Cleaning will begin now....\n")

        myCleaner = Cleaner()

        # Get all files to clean
        searchPath = "../data/rawData"
        countries = os.listdir(searchPath)
        positions = ["Associate", "Director", "Entry", "Internship", "Mid-Senior"]

        if self.format == "single":
            if self.manualFilePath:
                self.manualFilePath = self.manualFilePath.encode('unicode_escape')
                self.files.append(self.manualFilePath)
                myCleaner.startCleaner(self.manualFilePath)
                newPath = self.manualFilePath.replace("rawData", "cleanedData")
                print(f"Cleaned {self.manualFilePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n")
                self.files.append(newPath)
            else:
                raise ValueError("manualFilePath attribute cannot be empty when selecting single format")
        
        for country in countries:
            for position in positions:
                currPath = fr"{searchPath}/{country}/{position}"
                currPathFiles = os.listdir(currPath)
                if self.format == "all":
                    if len(currPathFiles) != 0:
                        for file in currPathFiles:
                            filePath = fr"{currPath}/{file}"
                            myCleaner.startCleaner(filePath)
                            newPath = filePath.replace("rawData", "cleanedData")
                            print(f"Cleaned {file} @ \n{filePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n")
                            self.files.append(newPath)

                elif self.format == "latestAll":
                    if len(currPathFiles) != 0:
                        # Get latest file
                        file = currPathFiles[-1]
                        filePath = fr"{currPath}/{file}"
                        newPath = filePath.replace("rawData", "cleanedData")
                        myCleaner.startCleaner(filePath)
                        print(f"Cleaned {file} @ \n{filePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n")
                        self.files.append(newPath)
                elif self.format == "single":
                    pass

                else: 
                    raise ValueError("Please enter a correct format value")

        print("Cleaning has ended...")
    
    def mergeFiles(self) -> None:
        '''
            Merges all files according to specified format attribute, adds merged file path into class attributes to be accessed by other functions.
            Parameters:
                None
            Returns:
                None
        '''
        myMerger = Merger()
        print("Merging in progress...")

        mergedDf = myMerger.merging_all_files(*self.files)
        mergedFileName = fr"{self.dateTime()}_MERGED"
        myMerger.createNewFile(mergedDf, mergedFileName)
        self.mergedFilePath = fr"../data/mergedData/{mergedFileName}.csv"
        print(f"Successfully merged file @\n{self.mergedFilePath}")

    def augmentFile(self) -> None:
        '''
            Augments merged file.
            Parameters:
                None
            Returns:
                None
        '''
        myAugmentor = Augmentor(self.mergedFilePath)
        augmentedFilePath = self.mergedFilePath.replace("mergedData", "augmentedData").replace("MERGED", "AUGMENTED")

        myAugmentor.augment()
        print(f"Successfully augmented file @\n{augmentedFilePath}")
    
    def process(self) -> None:
        '''
            Main function, cleans files according to format class attribute, merges them together, then augments data points, saving it to a new file.
            Parameters:
                None
            Returns:
                None
        '''
        self.cleanFiles()
        self.mergeFiles()
        self.augmentFile()

if __name__ == "__main__":
    # Example usage
    myProcessor = Processor(format="all")
    myProcessor.process()
