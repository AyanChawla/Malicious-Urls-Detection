from flask import Flask,request,jsonify,render_template,url_for,redirect
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
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

def predict(to_predict):
	model=joblib.load('logreg.pkl')
	x=model.predict(to_predict)
	return x
def trim(url):
    return re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', url).groups()[0]
app=Flask(__name__)
@app.route("/",methods=["POST",'GET'])
def index():
	
	return render_template("index.html")

@app.route('/prd',methods=['POST','GET'])
def prd():
	if request.method == 'POST'or 'GET':
		a=request.form.get('url')
		vectorizer = TfidfVectorizer(tokenizer=makeTokens)
		vectorizer=joblib.load('vec.pkl')
		X=vectorizer.transform([trim(a)])
		x=predict(X)
		if x=='1':
			prediction='This Url is Malicious'
		else:
			prediction='This Url is Normal'
	return render_template('prd.html',prediction=prediction)
if __name__ =='__main__':
    app.run(port=5000,debug=True)