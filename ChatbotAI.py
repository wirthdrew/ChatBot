#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:40:48 2019

@author: shalini
"""
from playsound import playsound
from gtts import gTTS 
import speech_recognition as sr
import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib 
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as webdriver
import os
from selenium.webdriver.common.keys import Keys
from textblob import TextBlob
#print(os.path.dirname(os.path.abspath(__file__)))
from tictactoeai import tictactoe 

class ai:
    def __init__(self):
        
        self.language = 'en'
        self.userinput = ''
        self.questions = {}
        #self.logresponses()
        self.logquestions()
        self.attempt = 0
        self.chrome_path =('/Users/andrew/Downloads/chromedriver') 
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--no-sandbox")   
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--window-size= 1080,1080" )
        self.players = ['x','o']
        self.saysomething = self.getinput()
        
    def ailogresponses(self, name, question):
        self.firstquestion = gTTS(text=question, lang=self.language, slow=False)
        self.firstquestion.save("{}.mp3".format(name)) 
        logquestion = {name : question}
        self.questions.update(logquestion)
     #   print(self.questions)
    def saysomething(self, question):
        playsound("{}.mp3".format(question)) 
        
    def getinput(self):
        self.userinput = ''
        r =sr.Recognizer()
        mic = sr.Microphone(device_index = 0)
     #   print(sr.Microphone.list_microphone_names())
        with mic as source:
            if self.attempt == 0:
                self.saysomething("InitialQuestion")
            else:
                self.saysomething("TryAgain")
            print("Say Something")
            audio = r.listen(source)
            
            print("Time over, Thanks")
        try:
            self.userinput = r.recognize_google(audio).lower()
            print(self.userinput)
        except:
            pass;
        if self.userinput == '':
            print("blank")
            self.saysomething("MissedQuestion")
            self.attempt +=1
            self.getinput()
        elif self.userinput in self.logquestion.keys():
            if self.userinput  == "play game":
                ttt =tictactoe()
                ttt.initializetictactoe()
                self.getinput()
            elif self.userinput == 'quit' or self.userinput == 'goodbye':
                self.saysomething(self.logquestion[self.userinput])
                return
            else:    
                self.saysomething(self.logquestion[self.userinput])
                self.getinput()
        
        elif self.userinput != '':
            print("userinput", self.userinput, type(self.userinput), len(self.userinput))
            self.decision = self.classifyquestion(str(self.userinput))
            self.saysomething(self.decision)
            self.search(self.decision)
       
        
        elif self.attempt > 1:
            self.attempt = 0
            return  
                
        else:
                self.saysomething("MissedQuestion")
                self.attempt +=1
                self.userinput = ''
                self.getinput()
            
        return self.userinput
        
    def listen(self):
        r =sr.Recognizer()
        mic = sr.Microphone(device_index = 0)
        print(sr.Microphone.list_microphone_names())
        with mic as source:
            if self.attempt == 0:
                pass
            else:
                self.saysomething("TryAgain")
            print("Say Something")
            audio = r.listen(source)
            
            print("Time over, Thanks")
        try:
            self.userinput = r.recognize_google(audio).lower()
            print(self.userinput)
        except:
            pass;
        if self.userinput == '':
            print("blank")
            self.saysomething("MissedQuestion")
            attempt +=1
            self.listen()        
        #elif self.attempt > 1:
        #    self.attempt = 0
        #    return   
                
        #else:
        #        self.saysomething("MissedQuestion")
        #        self.attempt +=1
        #        self.userinput = ''
        #        self.listen()
            
        return self.userinput
    
    
    def logresponses(self):
        logquestion = {   "StartOver" : "Im sorry I did not get that",
         "InitialQuestion" : "What can I help you with today? "
          , "MissedQuestion" : "I am sorry I didnt get that"
          ,"TryAgain" : "Lets try again what do you need help with?"
          , "Ben" : " Ben is a dork"
          , "purchase" : "I can help you with that purchase"
          , "question" : "I can help you with that question"
          , "SpaceTaken" : "That space has been taken "
          , "NewGame" : "This is a new game you can play by choosing a number between one and 9"
          , "PlayerTurn" : "It is your turn"
          , "AITurn" : " I went"
          , "Lose" : "You lose it is very difficult to beat me"
          , "Win" : "You win"
          ,"Introduction" : "I am a chat bot.  I am mostly a reflexive agent, with preprogrammed responses. However, through a machine learning algorithm I have learned to identify a question verses an intended purchase. We can also play tic tac toe using the mini max algorithm by simply saying play game"
          ,"Hello" : "hello"
          ,"Tie" : "The game is a Tie you are as smart as I"
          ,"PlayAgain" : "Do you want to play again yes or no"
          ,"GoodBye" : "Goodbye"
          }
        for key in logquestion:
           self.ailogresponses( key, logquestion[key])
           print(key, logquestion[key])
           
    def logquestions(self):
        self.logquestion = {   "what are your thoughts on ben" : "Ben"
          ,"what can you do" :"Introduction"
          ,"hello" : "Hello"  
          ,"play game" : "Launches a game"
          ,"goodbye":"GoodBye"
          ,"quit":"Goodbye"
          }
        
    def classifyquestion(self,testcon):
        QPcon = []
        QPcon.append(testcon)
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=joblib.load(open("vocab.pkl", "rb")))
        T = loaded_vec.transform(QPcon).toarray()
        print(T)
        knn_from_joblib = joblib.load('QPClassification.pkl')    
        print(knn_from_joblib.predict(T))  
        return knn_from_joblib.predict(T)[0]
    
    def search(self, action):
        self.browser = webdriver.Chrome(options=self.chrome_options, executable_path = self.chrome_path)
 
        if action == 'purchase':  
                 searchitem = (self.userinput)
                 print(searchitem)
                 blob = TextBlob(searchitem)
                 print(blob.tags)
                 nouns= []
                 for word,pos in blob.tags:
                     if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                         nouns.append(word)
                 self.browser.get("https://www.target.com/")
                 search = self.browser.find_element_by_id("search")
                 search.send_keys(nouns[len(nouns)-1])
                 search.send_keys(Keys.ENTER)
        if action == 'question':
                self.browser.get("https://www.Google.com/")
                search = self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input')
                search.send_keys(self.userinput)
                search.send_keys(Keys.ENTER)
                try:
                    answer =self.browser.find_element_by_xpath('//*[@class="Z0LcW"]')
                    print(answer.text)
                    self.ailogresponses('Answer', answer.text)
                    self.saysomething("Answer")
                except:
                    pass
               

        
            
question = ai()


