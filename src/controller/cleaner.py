from nltk import data
from nltk.util import pr
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pandas.core.frame import DataFrame
from nltk.stem.snowball import SnowballStemmer
#all user to run and download nltk by running the line below
#nltk.download()
#i tried using in function but no idea how (self) and ___init__ works
df = pd.read_csv("../models/data/2021_09_25_13_38_dataFile.csv")
#declare the language of stopwords to be removed in a set
stop_words = set(stopwords.words("english"))
print(stop_words)
#declare the language of stem to be used
stem_words = SnowballStemmer("english")
filtered_words =[]

#stemming the words before stop words removal, snowball stemming will automatically convert to lower case to remove 'The'
for i in range(0,len(df)):
    #stemming each data on the description using for loops
    stem_the_desc = stem_words.stem(df.loc[i][5])
    #update stem data back to the dataframe
    df.loc[i][5] = stem_the_desc
    #pull data from csv 'description', tokenize it to be a list with the value of each word
    list_of_desc = word_tokenize(df.loc[i][5])
    for w in list_of_desc:
        #for words that are not in the default stopwords will be appended into a new list
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


