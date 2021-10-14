from __future__ import annotations
import pandas as pd

"""
    Merger Module. Contains Merger Object, used for merging CSV files with identical columns
"""

class Merger:
    '''
        Merger object, used for merging CSV files with identical columns

        Class Attributes:
            None
    '''
    def __init__(self) -> Merger:
        '''
            Constructor for Merger Class.
            Parameters:
                None
            Returns:
                Merger => Constructs Merger Class
        '''
        pass
    
    def createNewFile(self, dataframe: pd.DataFrame, fileName: str) -> None:
        '''
            Constructor for Crawler Class.
            Parameters:
                dataframe : pd.DataFrame => merged dataframe to send to CSV file
                fileName : str => directory to store created CSV file
            Returns:
                None
        '''
        dataframe.to_csv(f"../data/mergedData/{fileName}.csv", index=False)


    def merging_all_files(self, *filePaths: str) -> pd.DataFrame:
        '''
            Merge all CSV files stored in directory
            Parameters:
                *filePaths : str => Filepath of each CSV file user wants to merge
            Returns:
                pd.DataFrame => Merged dataframe from all files
        '''
        merged_df = pd.DataFrame()
        for filePath in filePaths:
            curr_df = pd.read_csv(filePath)
            merged_df = merged_df.append(curr_df)

        return merged_df

if __name__ == "__main__":
    myMerger = Merger()
    merge_all_df = myMerger.merging_all_files(
        "../data/cleanedData/China/Mid-Senior/2021_10_10_15_21_Sales_dataFile.csv",
        "../data/cleanedData/Russia/Mid-Senior/2021_10_09_03_13_Sales_dataFile.csv",
        "../data/cleanedData/Singapore/Mid-Senior/2021_10_09_19_55_Sales_dataFile.csv",
        "../data/cleanedData/USA/Mid-Senior/2021_10_09_14_59_Sales_dataFile.csv"
        )
    myMerger.createNewFile(merge_all_df, "AllCountries_Mid-Senior_Data")
    