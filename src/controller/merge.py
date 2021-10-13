import pandas as pd
from datetime import datetime



class Merge:
    def __init__(self):
        pass
    
    def send_merge_df_to_analysis(self, clean_data_for_analysis):
        clean_data_for_analysis.to_csv("../views/analysisPlots/USA.csv", index=False)


    def merging_all_df(self, associatedata, directordata, entrydata, internshipdata,mid_seniordata):
        merged_df = pd.DataFrame()
        merged_df = merged_df.append(associatedata).append(directordata).append(entrydata).append(internshipdata).append(mid_seniordata)

        return merged_df

    def open_data_asso(self, filepath_asso):
        #filepath_asso = "../data/cleanedData/China/Associate/2021_10_10_07_00_Sales_dataFile.csv"
        return pd.read_csv(filepath_asso)

    def open_data_director(self, filepath_director):
        #filepath_director = "../data/cleanedData/China/Director/2021_10_09_16_58_Sales_dataFile.csv"
        return pd.read_csv(filepath_director)

    def open_data_entry(self, filepath_entry):
       # filepath_entry = "../data/cleanedData/China/Entry/2021_10_09_06_44_Sales_dataFile.csv"
        return pd.read_csv(filepath_entry)

    def open_data_intern(self, filepath_intern):
       # filepath_intern = "../data/cleanedData/China/Internship/2021_10_08_23_19_Sales_dataFile.csv"
        return pd.read_csv(filepath_intern)

    def open_data_mid_senior(self, filepath_mid_senior):
        #filepath_mid_senior ="../data/cleanedData/China/Mid-Senior/2021_10_10_15_21_Sales_dataFile.csv"
        return pd.read_csv(filepath_mid_senior)


if __name__ == "__main__":
    myMerge = Merge()
    asso_path = "../data/cleanedData/USA/Associate/2021_10_09_12_15_Sales_dataFile.csv"
    direct_path = "../data/cleanedData/USA/Director/2021_10_09_17_03_Sales_dataFile.csv"
    entry_path = "../data/cleanedData/USA/Entry/2021_10_09_09_30_Sales_dataFile.csv"
    intern_path = "../data/cleanedData/USA/Internship/2021_10_09_06_09_Sales_dataFile.csv"
    mid_path = "../data/cleanedData/USA/Mid-Senior/2021_10_09_14_59_Sales_dataFile.csv"
    associate = myMerge.open_data_asso(asso_path)
    director = myMerge.open_data_director(direct_path)
    entry = myMerge.open_data_entry(entry_path)
    internship = myMerge.open_data_intern(intern_path)
    mid_senior = myMerge.open_data_mid_senior(mid_path)
    merge_all_df = myMerge.merging_all_df(associate,director,entry,internship,mid_senior)
    myMerge.send_merge_df_to_analysis(merge_all_df)