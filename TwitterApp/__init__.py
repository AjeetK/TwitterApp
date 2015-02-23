from flask import Flask, render_template, request, redirect,url_for, abort, session, Response


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


app = Flask(__name__)


@app.route("/")

def main():
    return '''<div>start</div>
    <script>
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/fetch_tweet', true);
        xhr.onreadystatechange = function(e) {
            var div = document.createElement('div');
            div.innerHTML = '' + this.readyState + ':' + this.responseText;
            document.body.appendChild(div);
        };
        xhr.send();
    </script>
    '''


def hello():
	with open('list_of_languages.txt') as f:
		list_of_languages=[item for item in f]
	#list_of_languages = ["Java","JavaScript","PHP","Python","C#","C++","Ruby","CSS","C","Objective-C","Shell","Perl","R","Scala","Haskell","Matlab","Visual Basic","CoffeeScript","Clojure","Groovy","Go","Dart","Swift"]
	name = "Ajeet"
	return render_template("index.html",name=name,language_list=list_of_languages)


@app.route('/fetch_tweet', methods=['POST'])
def fetch_tweet():
	page_type = "got"
	
	
	
	lang_list = request.form.getlist('lang') 
	
	print lang_list
	#return render_template("index.html",lang_list=lang_list,page_type=page_type)
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	# with open('hashtags.txt') as hf:
	# 	hashtag = [line.strip() for line in hf]
	# 	print hashtag
	return Response(stream.filter(track=lang_list), mimetype='text/plain')
	


if __name__ == "__main__":
    app.run(debug=True)
