from flask import Flask, render_template, request, redirect,url_for, abort, session, Response

import json
import re
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "2507812099-Pj3dhFZl9CW40l0bwjxALA4Rv2MqksLey36Bw60"
access_token_secret = "3gMtceKmqLZdvvJqIBLkbrGlZ83tQi7ZcXEQpeycPSPP3"
consumer_key = "mlxnL0b3iPVo65Vwv8Sv4Pvf4"
consumer_secret = "VYq0PrbWGjxodAaEhI5wIatxWMpZZzOJ4KvC7R42l1Z0jIfPWE"





#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data
        with open('fetched_tweets.txt','a') as tf:
			tf.write(data)
        return True

    def on_error(self, status):
        print status

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

lang_list = []




app = Flask(__name__)
with open('list_of_languages.txt') as f:
		list_of_languages=[item for item in f]
@app.route("/")

# def main():
#     return '''<div>start</div>
#     <script>
#         var xhr = new XMLHttpRequest();
#         xhr.open('GET', '/fetch_tweet', true);
#         xhr.onreadystatechange = function(e) {
#             var div = document.createElement('div');
#             div.innerHTML = '' + this.readyState + ':' + this.responseText;
#             document.body.appendChild(div);
#         };
#         xhr.send();
#     </script>
#     '''


def hello():
	
	#list_of_languages = ["Java","JavaScript","PHP","Python","C#","C++","Ruby","CSS","C","Objective-C","Shell","Perl","R","Scala","Haskell","Matlab","Visual Basic","CoffeeScript","Clojure","Groovy","Go","Dart","Swift"]
	name = "Ajeet"
	return render_template("index.html",name=name,language_list=list_of_languages,page_type="start")


@app.route('/fetch_tweet', methods=['POST'])
def fetch_tweet():


	#page_type = "got"
	def tweets_related_to(word,text):
		#print text
		print word
		text = text.lower()
		word = word.lower()
		match = re.search(word, text)
		if match:
			print text
			return text
	if request.form.getlist('fetchbtn') == ['fetch']:
		global lang_list 
		lang_list = request.form.getlist('lang')
		stream.filter(track=lang_list, async=True)
		return render_template('index.html',page_type="fetching",lang_list=lang_list,language_list=list_of_languages)
	
	
	#return render_template("index.html",lang_list=lang_list,page_type=page_type)


	# with open('hashtags.txt') as hf:
	# 	hashtag = [line.strip() for line in hf]
	# 	print hashtag

	# print request.form.getlist('fetchbtn')
	if (request.form.getlist('stopbtn')) == ['stop']:
		print "inside stop"
		#lang_list = request.form.getlist('lang')
		print lang_list
		stream.disconnect()
		#return render_template("analyse.html")
		with open('fetched_tweets.txt') as tf:
			tweets = [json.loads(line).get('text') for line in tf]
			#print tweets
		print len(tweets)
		dict = {}
		for x in lang_list:
			dict[x] = filter(None,[tweets_related_to(x,tweet) for tweet in tweets])
		for x in dict:
			print dict[x]
		tweets_count = len(tweets)	
		page_type = "analyse"

		return render_template("analyse.html",page_type=page_type,dict=dict,total_tweets=tweets_count)
	# elif (request.form.getlist('fetchbtn')) == ['fetch']:
		#stream.filter(track=lang_list, async=True)
		#return render_template("index.html",page_type="fetching")
	#return "hello"
	


@app.route('/stop_fetching', methods=['POST'])
def stop_fetching():
	return render_template("analyse.html")

if __name__ == "__main__":
    app.run(debug=True)
