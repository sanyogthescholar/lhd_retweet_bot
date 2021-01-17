from twython import Twython
import sqlite3

CONSUMER_KEY = 'Your Key here'
CONSUMER_SECRET = 'Your Key here'
OAUTH_ACCESS_TOKEN = 'Your Key here'
OAUTH_ACCESS_TOKEN_SECRET = 'Your Key here'

t = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET)

search = t.search(q='#LocalHackDay', count=15)#Fetch the past 15 tweets with the hashtag

conn = sqlite3.connect('twitter.db')
cursor = conn.cursor()
tweets = search['statuses']

for tweet in tweets:
    id_tweet = tweet['id_str']
    cursor.execute("select count(*) from info where name=?;", (str(id_tweet),))#get the count of tweets if the tweet id exists in the database
    data = cursor.fetchall()
    if len(data) != 0: #I have honestly no idea how this works, but it does work
        try:
            conn.execute('insert into info values(?)', (str(id_tweet),))
        except sqlite3.IntegrityError:#If record already exists in database, then break the loop
            break
        t.create_favorite(id=id_tweet)
        t.retweet(id=id_tweet)
        continue
    else:
        continue
conn.commit()