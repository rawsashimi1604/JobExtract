import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Dataset (Plot 3)
datasetDataframe = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_All_Data.csv")

sns.set_theme(style="whitegrid")
# print(datasetDataframe)
datasetDataframe.rename(columns={'count':'keywordCount'}, inplace=True)
# SORTED 
plot3 = sns.barplot(x=(datasetDataframe.keyword),
            y=(datasetDataframe.keywordCount), 
            data=datasetDataframe, 
            order=datasetDataframe.sort_values('keywordCount',ascending = False).keyword)
plot3.set_xticklabels(plot3.get_xticklabels(), rotation=90)
plt.title("Total Count for Each Keyword")
plt.show()         

