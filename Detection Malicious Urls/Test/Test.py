from sklearn.externals import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import re
def makeTokens(f):
        tkns_BySlash = str(f.encode('utf-8')).split('/') # make tokens after splitting by slash\n",
        total_Tokens = []
        for i in tkns_BySlash:
            tokens = str(i).split('-')# make tokens after splitting by dash\n",
            tkns_ByDot = []
            for j in range(0,len(tokens)):
                temp_Tokens = str(tokens[j]).split('.')# make tokens after splitting by dot\n",
                tkns_ByDot = tkns_ByDot + temp_Tokens
            total_Tokens = total_Tokens + tokens + tkns_ByDot
        total_Tokens = list(set(total_Tokens))#remove redundant tokens\n",
        if 'https' in total_Tokens:
            total_Tokens.remove('https')
        if 'http' in total_Tokens:
            total_Tokens.remove('http')
        if 'com' in total_Tokens:
            total_Tokens.remove('com')#removing .com since it occurs a lot of times and it should not be included in our features\n",
        return total_Tokens
def trim(url):
    return re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', url).groups()[0]
def predict(to_predict):
	model=joblib.load('logreg.pkl')
	x=model.predict(to_predict)
	return x
######for individual Url
print('Enter Url')
url=str(input())
vectorizer = TfidfVectorizer(tokenizer=makeTokens)
vectorizer=joblib.load('vec.pkl')
X=vectorizer.transform([trim(url)])
x=predict(X)
print(x)
####if x is 0 then NORMAL, If x is 1 then MALICIOUS
x=pd.DataFrame(x)
x=x.to_json(r'individualurl.json')


####For Dataset
'''X_test=joblib.load('X_test.pkl')
y_test=joblib.load('y_test.pkl')
logreg=joblib.load('logreg.pkl')
pred=logreg.predict(X_test)
print(accuracy_score(y_test,pred))
pred=pd.DataFrame(pred)
pred=pred.to_json(r'dataseturl.json')'''
