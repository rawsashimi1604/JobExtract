import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Dataset (Plot 1)
datasetDataframe = pd.read_csv("../../data/mergedData/AllCountries_All_Data.csv")
sns.set_theme(style="whitegrid")
# print(datasetDataframe)

plot1 = sns.lineplot(x=(datasetDataframe.datePosted),
            y=(datasetDataframe.seniorityLevel), 
            data=datasetDataframe, 
            hue=datasetDataframe.location)
# plot1.set_xticklabels(plot1.get_xticklabels(), rotation=90)
plt.show()    
