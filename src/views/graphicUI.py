import sys
import pandas as pd
from pandasgui import show


sys.path.append("../")


def toshowalldata():
    ds = pd.read_csv("../data/cleanedData/Russia/All/2021_10_08_23_43_Sales_dataFile.csv")
    show(ds)




toshowalldata()

