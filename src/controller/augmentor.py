from __future__ import annotations
import os
import pandas as pd
from models.keywordsLook import KeywordsLookModel
import os

"""
    Augmentor Module. Contains Augmentor Object, augmenting new columns of data, mainly numerical to help with graph analysis.
"""

class Augmentor:
    '''
        Augmentor Object, augmenting new columns of data, mainly numerical to help with graph analysis.

        Class Attributes:
            filePath: str => File path of file to be augmented
    '''
    def __init__(self, filePath: str) -> Augmentor:
        '''
            Constructor for Augmentor Class.
            Parameters:
                filePath: str => File path of file to be augmented
            Returns:
                Augmentor => Constructs Augmentor Class
        '''
        self.filePath = filePath
    
    def augmentKeywordRatio(self) -> pd.DataFrame:
        '''
            Opens file in dataframe, and augments new columns with keyword ratio into it
            Parameters:
                None
            Returns:
                pd.DataFrame => Augmented dataframe
        '''

        df = pd.read_csv(self.filePath)
        descriptions = df['description']

        # New columns to be added to dataframe.
        dependenceRatio = []
        independenceRatio = []

        # List of words to be counted
        keywords = KeywordsLookModel()
        dependenceKeywords = keywords.dependenceKeywords
        independenceKeywords = keywords.independenceKeywords

        # Iterate through each description, calculate their ratio.
        for description in descriptions:
            dVal = self.calculateRatio(dependenceKeywords, description)
            iVal = self.calculateRatio(independenceKeywords, description)
            dependenceRatio.append(dVal)
            independenceRatio.append(iVal)
        
        # Append to dataframe
        df['dependenceRatio'] = dependenceRatio
        df['independenceRatio'] = independenceRatio

        return df

    @staticmethod
    def calculateRatio(wordList: list, description: str) -> float:
        '''
            Calculates ratio of words based on number of occurence in word list.
            Parameters:
                wordList: list => Word list to look up words in
                description: str => 
            Returns:
                float => Ratio of occurence to word list
        '''
        count = 0
        descriptionList =  description.split(" ")
        for word in set(descriptionList):
            if word in wordList:
                count += 1
        
        # Scale based on number of words appearing in description
        val = ((count / len(wordList)) / len(descriptionList)) * 100
        return val

    def augment(self) -> None:
        '''
            Main function to augment CSV, saves to new location
            Parameters:
                None
            Returns:
                None
        '''
        df = self.augmentKeywordRatio()
        fileName = self.filePath.split("/")[-1]
        df.to_csv(f"../data/augmentedData/{fileName}", index=False)


if __name__ == "__main__":
    myAugmentor = Augmentor("../data/mergedData/AllCountries_All_Data.csv")
    myAugmentor.augment()

