import pandas as pd
from datetime import datetime



class Merger:
    def __init__(self):
        pass
    
    def send_merge_df_to_analysis(self, clean_data_for_analysis, fileName):
        clean_data_for_analysis.to_csv(f"../views/analysisDatasets/{fileName}.csv", index=False)


    def merging_all_df(self, associatedata, directordata, entrydata, internshipdata,mid_seniordata):
        merged_df = pd.DataFrame()
        merged_df = merged_df.append(associatedata).append(directordata).append(entrydata).append(internshipdata).append(mid_seniordata)

        return merged_df

    def open_data(self, filepath):
        return pd.read_csv(filepath)


if __name__ == "__main__":
    myMerger = Merger()
    asso_path = "../data/cleanedData/USA/Associate/2021_10_09_12_15_Sales_dataFile.csv"
    direct_path = "../data/cleanedData/USA/Director/2021_10_09_17_03_Sales_dataFile.csv"
    entry_path = "../data/cleanedData/USA/Entry/2021_10_09_09_30_Sales_dataFile.csv"
    intern_path = "../data/cleanedData/USA/Internship/2021_10_09_06_09_Sales_dataFile.csv"
    mid_path = "../data/cleanedData/USA/Mid-Senior/2021_10_09_14_59_Sales_dataFile.csv"
    associate = myMerger.open_data(asso_path)
    director = myMerger.open_data(direct_path)
    entry = myMerger.open_data(entry_path)
    internship = myMerger.open_data(intern_path)
    mid_senior = myMerger.open_data(mid_path)
    merge_all_df = myMerger.merging_all_df(associate,director,entry,internship,mid_senior)
    myMerger.send_merge_df_to_analysis(merge_all_df)