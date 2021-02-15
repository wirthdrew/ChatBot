#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 21:49:08 2019

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
import numpy as np
from math import inf as infinity

class aicopy:
    def __init__(self):
        
        self.language = 'en'
        self.userinput = ''
        self.questions = {}
        self.logquestions()
        self.attempt = 0
        self.chrome_path =('/Users/shalini/Fall2019_AW/FoundationsofAI/Homework/FinalProject/chromedriver') 
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--no-sandbox")   
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--window-size= 1080,1080" )
        self.players = ['x','o']
       # self.saysomething = self.getinput()
        
    def saysomething(self, question):
        playsound("{}.mp3".format(question)) 
        
    def getinput(self):
        r =sr.Recognizer()
        mic = sr.Microphone(device_index = 0)
        print(sr.Microphone.list_microphone_names())
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
            if self.userinput  == "start tic-tac-toe":
                ttt =tictactoe()
                print(launctictactoe)
            else:    
                self.saysomething(self.logquestion[self.userinput])
        
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
            self.attempt +=1
            self.listen()                    
        return self.userinput
    
    
    def logresponses(self):
        logquestion = {   "StartOver" : "Im sorry I did not get that",
         "InitialQuestion" : "What can I help you with today? You can say something like buy socks"
          , "MissedQuestion" : "I am sorry I didnt get that"
          ,"TryAgain" : "Lets try again what do you need help with?"
          , "Ben" : " Ben is a dork"
          , "purchase" : "I can help you with that purchase"
          , "question" : "I can help you with that question"
          , "SpaceTaken" : "That space has been taken "
          , "NewGame" : "This is a new game you can play by choosing a number between one and 9"
          , "PayerTurn" : "It is your turn"
          , "AI Turn" : " I choose blank"
          , "Lose" : "You lose it is very difficult to beat me"
          , "Win" : "You win how by my calculations"
          ,"Introduction" : "I am a sentient agent just kidding"
          ,"Hello" : "hello"
          }
        for key in logquestion:
           self.ailogresponses( key, logquestion[key])
           print(key, logquestion[key])
           
    def logquestions(self):
        self.logquestion = {   "what are your thoughts on ben" : "Ben"
          ,"what can you do" :"Introduction"
          ,"hello" : "Hello"  
          ,"start tic-tac-toe" : "Launches a game"
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
                search = self.browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
                search.send_keys(self.userinput)
                search.send_keys(Keys.ENTER)
                try:
                    answer =self.browser.find_element_by_xpath('//*[@class="Z0LcW"]')
                    print(answer.text)
                    self.ailogresponses('Answer', answer.text)
                    self.saysomething("Answer")
                except:
                    pass





class tictactoe(aicopy):
    def __init__(self):
    
        self.players = ['x','o']
        self.attempt = 0
        self.userinput = '' 
    
    def action(self, state, player, block_num):
        if state[int((block_num-1)/3)][(block_num-1)%3] is ' ':
            state[int((block_num-1)/3)][(block_num-1)%3] = player
        else:
            self.saysomething("SpaceTaken")
            block_num = int(self.listen())
            print(block_num, type(block_num))
            self.action(state, player, int(block_num))
        
    def state2(self, state):
        nextstate = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        for i in range(3):
            for j in range(3):
                nextstate[i][j] = state[i][j]
        return nextstate
        
    def state(self,gamegrid):
        Tie_flag = 0
        for i in range(3):
            for j in range(3):
                if gamegrid[i][j] is ' ':
                    Tie_flag = 1
        if Tie_flag is 0:
            return None, "Tie"
        
        if (gamegrid[0][0] == gamegrid[0][1] and gamegrid[0][1] == gamegrid[0][2] and gamegrid[0][0] is not ' '):
            return gamegrid[0][0], "Done"
        if (gamegrid[1][0] == gamegrid[1][1] and gamegrid[1][1] == gamegrid[1][2] and gamegrid[1][0] is not ' '):
            return gamegrid[1][0], "Done"
        if (gamegrid[2][0] == gamegrid[2][1] and gamegrid[2][1] == gamegrid[2][2] and gamegrid[2][0] is not ' '):
            return gamegrid[2][0], "Done"
        if (gamegrid[0][0] == gamegrid[1][0] and gamegrid[1][0] == gamegrid[2][0] and gamegrid[0][0] is not ' '):
            return gamegrid[0][0], "Done"
        if (gamegrid[0][1] == gamegrid[1][1] and gamegrid[1][1] == gamegrid[2][1] and gamegrid[0][1] is not ' '):
            return gamegrid[0][1], "Done"
        if (gamegrid[0][2] == gamegrid[1][2] and gamegrid[1][2] == gamegrid[2][2] and gamegrid[0][2] is not ' '):
            return gamegrid[0][2], "Done"
        if (gamegrid[0][0] == gamegrid[1][1] and gamegrid[1][1] == gamegrid[2][2] and gamegrid[0][0] is not ' '):
            return gamegrid[1][1], "Done"
        if (gamegrid[2][0] == gamegrid[1][1] and gamegrid[1][1] == gamegrid[0][2] and gamegrid[2][0] is not ' '):
            return gamegrid[1][1], "Done"
        
        return None, "Not Done"
    
    def printState(self,gamegrid):
        print('----------------')
        print('| ' + str(gamegrid[0][0]) + ' | ' + str(gamegrid[0][1]) + ' | ' + str(gamegrid[0][2]) + ' |')
        print('----------------')
        print('| ' + str(gamegrid[1][0]) + ' | ' + str(gamegrid[1][1]) + ' | ' + str(gamegrid[1][2]) + ' |')
        print('----------------')
        print('| ' + str(gamegrid[2][0]) + ' | ' + str(gamegrid[2][1]) + ' | ' + str(gamegrid[2][2]) + ' |')
        print('----------------')
        
        
    def AIMove(self,state, player):
        winstatus_loser , done = self.state(state)
        if done == "Done" and winstatus_loser == 'O': 
            return 1
        elif done == "Done" and winstatus_loser == 'X': 
            return -1
        elif done == "Tie":    
            return 0
            
        moves = []
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j] is ' ':
                    empty_cells.append(i*3 + (j+1))
        
        for empty_cell in empty_cells:
            move = {}
            move['index'] = empty_cell
            nextstate = self.state2(state)
            self.action(nextstate, player, empty_cell)
            
            if player == 'O':  
                result = self.AIMove(nextstate, 'X')    
                move['score'] = result
            else:
                result = self.AIMove(nextstate, 'O')   
                move['score'] = result
            
            moves.append(move)
        aimove = None
        if player == 'O':   
            best = -infinity
            for move in moves:
                if move['score'] > best:
                    best = move['score']
                    aimove = move['index']
        else:
            best = infinity
            for move in moves:
                if move['score'] < best:
                    best = move['score']
                    aimove = move['index']
                    
        return aimove
    
    def initializetictactoe(self):
        chance = 'Y'
        while chance == 'Y' or chance == 'y':
            gamegrid = [[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']]
            currenturn = "Not Done"
            self.printState(gamegrid)
            chooseplayer = "X"
            winstatus = None
            
            if chooseplayer == 'X' or chooseplayer == 'x':
                playerturn = 0
            else:
                playerturn = 1
                
            while currenturn == "Not Done":
                if playerturn == 0: # Human's turn
                    #int(input("Oye Human, your turn! Choose where to place (1 to 9): "))
                    self.saysomething("PlayerTurn")
                    block_choice = int(self.listen())
                    self.action(gamegrid , self.players[playerturn], block_choice)
                else:   # AI's turn
                    block_choice = self.AIMove(gamegrid, self.players[playerturn])
                    self.action(gamegrid ,self.players[playerturn], block_choice)

                self.printState(gamegrid)
                if playerturn !=0:
                    self.saysomething("AITurn")
                winstatus, currenturn = self.state(gamegrid)
                if winstatus is not None:
                    if winstatus == 'X':
                        self.saysomething("Win") 
                    else:
                        self.saysomething("Lose") 
                else:
                    playerturn = (playerturn + 1)%2    
                if currenturn is "Tie":
                    self.saysomething("Tie")                  
            self.saysomething("PlayAgain") 
            chance = self.listen()
            if chance == 'no':
                self.saysomething("GoodBye") 