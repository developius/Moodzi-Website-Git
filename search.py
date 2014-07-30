from TwitterSearch import *
import delorean
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

def check_twitter(query):
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.setKeywords([query]) # let's define all words we would like to have a look for
        tso.setLanguage('en') # we want to see German tweets only
        #tso.setCount(1000000) # please dear Mr Twitter, only give us 7 results per page
        tso.setIncludeEntities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'A4yyJgy9yY0mcJDQn4LXhrjcz',
            consumer_secret = 'ID6luLGLOUCx9ADVl77IysKibEblDhuwS6sehQ3SUuEB3ZNsoW',
            access_token = '2689652840-K2dw8nIKu7VJHrW6snsOOeFZFiEGqd5wPAaLm9V',
            access_token_secret = 'oB0KjuzAv9bGSaPbDA0Ate7mXfnmhh94ff9x2EGQjcY0e'
         )

        now_time = delorean.parse(str(datetime.utcnow()))
        now_time_minute = now_time._dt.time().minute
        now_time_hour = now_time._dt.time().hour

        cont = True

        i = 0
        average_retweets = 0
        biggest_no_of_retweets = 0

        for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
            tweet_time_minute = delorean.parse(ts.getMetadata()['date'])._dt.time().minute
            tweet_time_hour = delorean.parse(ts.getMetadata()['date'])._dt.time().hour
            if (tweet_time_hour + 1 == now_time_hour) and ((now_time_minute - tweet_time_minute) <= 2):
                average_retweets += tweet['retweet_count']
                if tweet['retweet_count'] >= biggest_no_of_retweets:
                    biggest_no_of_retweets = tweet['retweet_count']
                #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
                i +=1
                #print '.'
            else:
                break

        average_retweets = average_retweets / i
        return 'the biggest number of retweets was ' + str(biggest_no_of_retweets) + ' and the average number of retweets out of ' + str(i) + ' tweets was ' + str(average_retweets) 




    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/query/<query>')
def check_twitter_page(query):
    return check_twitter(query)

if __name__ == '__main__':
    app.run(debug = True)
