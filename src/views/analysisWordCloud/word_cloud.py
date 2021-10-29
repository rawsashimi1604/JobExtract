from tkinter import Label
import pandas as pd
import numpy as np
from wordcloud import (WordCloud, get_single_color_func)
from PIL import Image
import matplotlib.pyplot as plt

'''
    WordCloud Image
'''

# Dataset (WordCloud)
datasetDataframe = pd.read_csv("../../data/keywords/KEYWORDS_AllCountries_All_Data.csv")

df_keyword = []
df_count =[]
df_type = []
df_keyword = datasetDataframe.get(key='keyword').tolist()

df_count = datasetDataframe.get(key='count').tolist()
df_type = datasetDataframe.get(key='type_').tolist()


df_dict = dict(zip(df_keyword,df_count))

wordcloud = WordCloud(background_color='white',
                      width=1500,
                      height=1000
                      ).generate_from_frequencies(df_dict)
# use .generate(space_separated_string) - to generate cloud from text

plt.figure(figsize=(15,13))
plt.imshow(wordcloud, interpolation='bilInear')
plt.axis('off')
plt.show()
