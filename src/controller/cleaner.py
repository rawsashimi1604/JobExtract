from nltk import data
from nltk.util import pr
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pandas.core.frame import DataFrame
#all user to run and download nltk by running the line below
#nltk.download()

df = pd.read_csv("../models/data/2021_09_25_13_38_dataFile.csv")
stop_words = set(stopwords.words('english'))
filtered_words =[]

for i in range(0,len(df)):
    list_of_desc = word_tokenize(df.loc[i][5])
    for w in list_of_desc:
        if w not in stop_words:
            filtered_words.append(w)
    #appended words are in list so we joined it and convert it to str        
    filtered_data_to_go_back_into_df = ", ".join(map(str, filtered_words)).replace(",","")
    #update the column with the new filtered string
    df.loc[i][5] = filtered_data_to_go_back_into_df
    df.to_csv("../models/data/2021_09_25_13_38_dataFile.csv", index=False)
    #to display changes made in csv only for first data since i make a break, u can remove it for now we need to use function so dun remove it yet
    print(df.loc[0][5])
    break


