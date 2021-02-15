



import pandas as pd
import random 
filename = 'S08_question_answer_pairs.txt'

questions = pd.read_csv(filename, sep='\t', lineterminator='\n', header = None)

questions = questions.drop(columns=[0, 2, 3, 4, 5])

classification = ['question']*1715 
questions['Classification'] = classification
cleandata = pd.read_csv('PurchaseDataset.csv', header = None)
x = cleandata[1].to_list()
y = cleandata[2].to_list()

finishedlist = []

for i in x:
    for s in y:
        try:
            m = i.lower() + ' ' + s.lower()
            finishedlist.append(m)
        except:
            continue
random.shuffle(finishedlist)
finishedlist = finishedlist[:1750]
purchasecol = pd.Series(finishedlist)
purchasecol = pd.DataFrame(purchasecol)
classification = ['purchase']*1750 
purchasecol['Classification'] = classification

finaltrainingset = pd.concat([questions, purchasecol])
print(finaltrainingset)
finaltrainingset.to_csv('testtrainingset.csv')
