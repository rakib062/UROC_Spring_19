import csv
import re


class Stats:
    def __init__(self, api, dicts):
        """
        Constructor for the class to print the statistics of the data
        :param api: setup api wrapper class form tweet collection class
        :param dicts: list of dictionaries {tweet id : replies} from collection
        """
        self.api = api
        self.dicts = dicts
        self.words = []  # to hold number of words for each tweet. len(words) = # tweets sum(words) = # words
        self.replies = []
        self.tweets = []

    def get_data(self):
        """
        Function to collect all the statistics on the data and write it to a csv file
        :return:
        """
        def write(id, t):
            """
            Function to write an data point as an id and text to  a CSV file
            :param id: tweet id
            :param t: text of tweet (already cleaned)
            :return:
            """
            writer = csv.writer(open('data.csv', mode='a'), delimiter=',', quotechar='"')
            writer.writerow([str(id), str(len(t.split())), t])

        def remove_hashtags_links(text):
            '''
            Function using regex to remove hashtags and links from a given tweet
            found at: https://tinyurl.com/y2j8ydptd  ss
            Doesnt always work perfectly. sometimes only removes the # and leaves the word following it
            :param text: text to clean of hashtags and links
            :return: cleaned text
            '''
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        print("Collecting tweets by ID...")
        # loop through dictionaries and grab all the parent tweets based on ids
        dictnum = 1
        for dict in self.dicts:
            ids = list(dict.keys())
            i = 0
            # grab tweets in chunks of 100
            while i+100 < len(ids):
                self.tweets.extend(self.api.get_tweets_from_ids(ids[i:i+100]))
                i += 100
            else: self.tweets.extend(self.api.get_tweets_from_ids(ids[i:]))
            print("done with dict number " + str(dictnum))
            dictnum += 1
        print("Tweets collected...")

        # loop through all tweets
        for tweet in self.tweets:
            # grab text and id from tweet and clean the text
            if "retweeted_status" in dir(tweet):
                text, id = tweet.retweeted_status.full_text, tweet.retweeted_status.id
                text = remove_hashtags_links(text)
            else:
                text, id = tweet.full_text, tweet.id
                text = remove_hashtags_links(text)

            # save number of words from a tweet
            self.words.append(len(text.split()))
            # write(id, text)

            # get dict that contains tweet id
            for dict in self.dicts:
                if id in list(dict.keys()):
                    d = dict
                    break

            # save number of replies of the tweet
            self.replies.append(len(d[id]))
            # for each reply get the text and id and clean the text
            for rep in d[id]:
                text = remove_hashtags_links(rep['full_text'])
                self.words.append(len(text.split()))
                # write(rep['id'], text)

    def print(self):
        """
        Function to print out stats of data
        :return:
        """
        parent_tweets = len(self.tweets)  # num parent tweets
        replies = sum(self.replies)   # num replies
        tweets = parent_tweets + replies   # total num tweets
        avg_replies = replies/parent_tweets   # average num of replies per parent tweet
        avg_words = sum(self.words)/tweets   # average number of words per tweet

        print("\ntotal number of parent tweets: " + str(parent_tweets))
        print("total number of replies: " + str(replies))
        print("total number of tweets: " + str(tweets))
        print("average replies per tweet: " + str(avg_replies))
        print("average words per tweet: " + str(avg_words))
