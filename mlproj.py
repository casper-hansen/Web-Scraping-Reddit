import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(binary=True)

df = pd.read_csv('data/r-machinelearning_r-datascience.csv')

print(df.head(5))