import copy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

pd.options.mode.chained_assignment = None
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
    second = df.score.quantile(0.50) # Average
    third = df.score.quantile(0.75) # Good
    fourth = df.score.quantile(0.95) # exceptional
    
    new_score = []
    
    for i, row in enumerate(df.score):
        if row > fourth:
            new_score.append('exceptional')
        elif row > third:
            new_score.append('good')
        elif row > second:
            new_score.append('average')
        else:
            new_score.append('bad')
        
    df.score = new_score
    
    #df = pd.get_dummies(df, columns=['score'])
    
    return df

def df_split(df):
    y = df[['score']]
    X = df.drop(['score'], axis=1)
    
    content = [' ' + comment for comment in X.text.values]
    X = CountVectorizer().fit_transform(content).toarray()
    
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)
    
    return X_train, X_test, y_train, y_test

df = prepare_data(df)
df = score_to_percentile(df)

X_train, X_test, y_train, y_test = df_split(df)

lr = LogisticRegression(C=0.05, solver='lbfgs', multi_class='multinomial')
lr.fit(X_train, y_train)
pred = lr.predict(X_test)
score = accuracy_score(y_test, pred)

print ("Accuracy: {0}".format(score))