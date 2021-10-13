import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Apply the default theme
sns.set_theme()

# Load a dataset
crash_df = sns.load_dataset("car_crashes")
myKeywords = "../../data/keywords/SINGAPORE_2021_09_29_21_34_Sales_dataFile_keywords.csv"
myData = pd.read_csv(myKeywords)

sns.barplot(x="type_", y="count", data=myData)

# Styling
# sns.set_style('ticks')
# sns.set_context('paper', font_scale=1.2)
# sns.jointplot(x="speeding", y="alcohol", data=crash_df, kind="reg")

plt.show()
