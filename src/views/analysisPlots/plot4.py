import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def countValues(dataframe, countParameter, filterParameter, columnName):
    '''
        Counts total value of dataframe after filtering
    '''
    df = dataframe.loc[dataframe[columnName] == filterParameter]
    return df[countParameter].sum()

def count(dataframe):
    return len(dataframe.index)

def constructDataset():
    # Dataset (Plot 2)
    associateKwDataFrame = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_Associate_Data.csv")
    directorKwDataFrame = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_Director_Data.csv")
    entryKwDataFrame = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_Entry_Data.csv")
    internshipKwDataFrame = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_Internship_Data.csv")
    midseniorKwDataFrame = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_Mid-Senior_Data.csv")

    associateDataFrame = pd.read_csv("../../data/mergedData/AllCountries_Associate_Data.csv")
    directorDataFrame = pd.read_csv("../../data/mergedData/AllCountries_Director_Data.csv")
    entryDataFrame = pd.read_csv("../../data/mergedData/AllCountries_Entry_Data.csv")
    internshipDataFrame = pd.read_csv("../../data/mergedData/AllCountries_Internship_Data.csv")
    midseniorDataFrame = pd.read_csv("../../data/mergedData/AllCountries_Mid-Senior_Data.csv")

    # Store all data in JSON FORMAT
    keywordsData = {
        "Data" : 
        {
            "Associate" : {
                "dependenceCount": countValues(associateKwDataFrame, "count", "dependence", "type_"),
                "independenceCount": countValues(associateKwDataFrame, "count", "independence", "type_"),
                "dataCount": count(associateDataFrame)
            },
            
            "Director" : {
                "dependenceCount": countValues(directorKwDataFrame, "count", "dependence", "type_"),
                "independenceCount": countValues(directorKwDataFrame, "count", "independence", "type_"),
                "dataCount": count(directorDataFrame)
            },

            "Entry" : {
                "dependenceCount": countValues(entryKwDataFrame, "count", "dependence", "type_"),
                "independenceCount": countValues(entryKwDataFrame, "count", "independence", "type_"),
                "dataCount": count(entryDataFrame)
            },

            "Internship" : {
                "dependenceCount": countValues(internshipKwDataFrame, "count", "dependence", "type_"),
                "independenceCount": countValues(internshipKwDataFrame, "count", "independence", "type_"),
                "dataCount": count(internshipDataFrame)
            },

            "Mid-Senior" : {
                "dependenceCount": countValues(midseniorKwDataFrame, "count", "dependence", "type_"),
                "independenceCount": countValues(midseniorKwDataFrame, "count", "independence", "type_"),
                "dataCount": count(midseniorDataFrame)
            }
        }
    }

    # CONSTRUCT THE COMPILED DATA SET
    # Seniority levels in increasing order
    seniorityLevels = ["Internship", "Entry", "Associate", "Mid-Senior", "Director"]

    # Column names
    columns = ["seniorityLevel", "seniorityCount", "dependence", "independence"]


    # Create Data
    data = []
    for level in seniorityLevels:
        rowDict = {
            "seniorityLevel": level,
            "seniorityCount": keywordsData["Data"][level]["dataCount"],
            "dependence": keywordsData["Data"][level]["dependenceCount"],
            "independence": keywordsData["Data"][level]["independenceCount"],
        }
        data.append(rowDict)

    # FINAL DATASET
    datasetDataframe = pd.DataFrame(columns=columns, data=data)
    return datasetDataframe