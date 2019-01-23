from api_wrapper  import *
import pickle

api = API(Auth(ck, cs, ak, acs)) #fill the parameters of the Auth object
tweets = api.search_tweets(query='#TrumpShutdown', since="2018-01-20", page_count=1)
print(len(tweets), ' tweets were collected')

#save the tweets
pickle.dump(tweets, open('filename','wb'))
