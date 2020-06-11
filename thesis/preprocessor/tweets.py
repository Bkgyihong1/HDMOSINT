# cleaning the tweet data
from os import listdir
from os.path import isfile, join

import pandas as pd
import pickle
import json
import re
import string
from sklearn.feature_extraction.text import CountVectorizer


class preprocess_tweets:
    def __init__(self):
        run = self.check()
        if run == 0:
            self.tweets()
        else:
            print("No textual data")
        print("Preprocessed tweet data")

    def check(self):
        # search for presence of file
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            x = 0
            if file != "tweets.json":
                x += 1
                continue
            elif file != "tweets.json" and x == len(files):
                return "none"
            else:
                x = 0
                return x

    def combine_tweets(self, list_of_tweets):
        """
        the dictionary is currently in the format of
        key: tweets, value: list of all the recent collected tweets
        and now changing it to
        key: tweets, value : string
        """
        combined_tweets = ''.join(list_of_tweets)
        return combined_tweets

    # first round of cleaning the text
    def clean_text_round1(self, text):
        """
        Make text lowercase,
        remove text in square brackets, remove punctuation and remove words containing numbers.
        """
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        text = re.sub(r"http\S+", '', text)
        return text

    # Apply a second round of cleaning
    def clean_text_round2(self,text):
        """
        Get rid of some additional punctuation and non-sensical text
        that was missed the first time around.
        """
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    def tweets(self):
        target = ["Target"]
        with open("../raw_data/tweets.json", "r") as f:
            tweet_data = json.load(f)
        tweet = tweet_data['tweets']

        # save tweet to text file
        for tweet, c in enumerate(target):
            with open("../clean_data/tweets.txt", "wb") as file:
                pickle.dump(tweet_data['tweets'], file)

        # load the tweets
        data = {}
        with open("../clean_data/tweets.txt", "rb") as file:
            data['tweets'] = pickle.load(file)

        # combining the tweets
        data_combined = dict()

        for key, value in data.items():
            data_combined[key] = self.combine_tweets(value)
        # print(data_combined)

        # Converting from dictionary format to DataFrame
        data_df = pd.DataFrame(data_combined, index=['tweets']).transpose()
        data_df.columns = ['tweet_data']
        data_df = data_df.sort_index()
        data_df.to_pickle("../pickles/corpus.pkl")  # original data pickle

        round1 = lambda x: self.clean_text_round1(x)
        data_clean = pd.DataFrame(data_df.tweet_data.apply(round1))
        round2 = lambda x: self.clean_text_round2(x)
        data_clean = pd.DataFrame(data_clean.tweet_data.apply(round2))
        # print(data_clean.tweet_data.loc['tweets'])  # the cleaned content in under tweets column

        """
        create a document-term matrix using CountVectorizer,
        and exclude common English stop words
        """
        cv = CountVectorizer(stop_words='english')
        data_cv = cv.fit_transform(data_clean.tweet_data)
        # Convert it to an array and label all the columns
        data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_dtm.index = data_clean.index

        # (before we put it in document-term matrix format) and the CountVectorizer object
        data_clean.to_pickle('../pickles/data_clean.pkl')
        pickle.dump(cv, open("../pickles/cv.pkl", "wb"))

        data_dtm.to_pickle("../pickles/dtm.pkl")

