from api_wrapper  import *
import pickle

api = API(Auth(ck, cs, ak, acs)) #fill the parameters of the Auth object
tweets = api.search_tweets(query='#TrumpShutdown', since="2018-01-20", page_count=1)
print(len(tweets), ' tweets were collected')

#save the tweets
pickle.dump(tweets, open('filename','wb'))


#example of collecting replis
def tweepy_to_twarc(tweet):
	'''Convert tweepy status object to a dictionary'''
	tw = dict()
	tw['id'] = tweet.id
	tw['id_str'] = str(tweet.id)
	tw['user'] = dict()
	tw['user']['screen_name'] = tweet.user.screen_name
	return tw

twarc = Twarc(auth.ck, auth.cs, auth.ak, auth.acs)

replies = []
reps = twarc.replies(tweepy_to_twarc(tweet), recursive= True)
rep = next(reps)
while True:
    try: 
        rep = next(reps)
        replies.append(rep)
    except StopIteration:
        break
    except Exception as e:
        print('error: ',e)
 print(len(replies), ' replies collected')
