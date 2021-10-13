import pandas as pd
from datetime import datetime



class Merger:
    def __init__(self):
        pass
    
    def createNewFile(self, clean_data_for_analysis, fileName):
        clean_data_for_analysis.to_csv(f"../data/mergedData/{fileName}.csv", index=False)


    def merging_all_files(self, *filePaths):
        merged_df = pd.DataFrame()
        for filePath in filePaths:
            curr_df = self.open_data(filePath)
            merged_df = merged_df.append(curr_df)

        return merged_df

    def open_data(self, filepath):
        return pd.read_csv(filepath)


if __name__ == "__main__":
    myMerger = Merger()
    merge_all_df = myMerger.merging_all_files(
        "../data/cleanedData/China/Mid-Senior/2021_10_10_15_21_Sales_dataFile.csv",
        "../data/cleanedData/Russia/Mid-Senior/2021_10_09_03_13_Sales_dataFile.csv",
        "../data/cleanedData/Singapore/Mid-Senior/2021_10_09_19_55_Sales_dataFile.csv",
        "../data/cleanedData/USA/Mid-Senior/2021_10_09_14_59_Sales_dataFile.csv"
        )
    myMerger.createNewFile(merge_all_df, "AllCountries_Mid-Senior_Data")