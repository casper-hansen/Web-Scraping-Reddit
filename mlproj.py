import copy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/comment_data.csv', usecols=['score', 'text'])

def prepare_data(df):
    # Remove everything except alphanumeric characters
    df.text = df.text.str.replace('[^a-zA-Z\s]', '')
    
    # Get only numbers, but allow minus in front
    df.score = df.score.str.extract('(^-?[0-9]*\S+)')
    
    # Remove rows with None as string
    df.score = df.score.replace('None', np.nan)
    
    # Remove all None
    df = df.dropna()
    
    # Convert score feature from string to float
    score = df.score.astype(float)
    df.score = copy.deepcopy(score)
    
    return df

def score_to_percentile(df):
    a = df.score.quantile(0.25)
    
    b = df.score.quantile(0.50) 
    
    c = df.score.quantile(0.75) 
    
    d = df.score.quantile(0.9)
    
    print(d)
    
    return df

def df_split(df):
    y = df.score
    X = df.drop(['score'], axis=1)
    
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)
    
    return X_train, X_test, y_train, y_test

df = prepare_data(df)
df = score_to_percentile(df)


#X_train, X_test, y_train, y_test = df_split(df)