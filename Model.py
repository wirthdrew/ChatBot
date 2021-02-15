# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 11:41:07 2019

@author: gyoxwir
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib 


dataset = pd.read_csv('trainingset.csv', encoding = "ISO-8859-1")#'NarrowData_ ManualReview.xlsx')

conversations = dataset
listofconversations= []

for conversation in conversations['Questions']:
    listofconversations.append(conversation)

#print(listofconversations)    
#vectorizer = CountVectorizer(min_df=0, lowercase=True)
#vectorizer.fit(listofconversations)
#print(vectorizer.vocabulary_)
matrix = CountVectorizer(max_features=2000, lowercase =True)#1000)
X = matrix.fit_transform(listofconversations).toarray()


print(matrix.vocabulary_)
joblib.dump(matrix.vocabulary_,open("vocab.pkl","wb"))


testcon =['What is an abraham licoln'] 
#matrix = CountVectorizer(max_features=2000)#1000)
T = matrix.transform(testcon).toarray()
print(T)
#print(X)
#print(X.shape)
y = dataset.iloc[:, 0]
#print(y)
# split train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y)
#print(X_test)
# Naive Bayes 
classifier = GaussianNB()
classifer = classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
#print(accuracy)   
if accuracy >=.5:    
    print(accuracy)
    # Save the model as a pickle in a file 
    joblib.dump(classifier, 'QPClassification.pkl')   
    # Load the model from the file 
    knn_from_joblib = joblib.load('QPClassification.pkl')    
    # Use the loaded model to make predictions 
    print(knn_from_joblib.predict(T))     
    
    
    
    