"""
show target's semantic change over time via tweets,
Polarity and Subjectivity

"""
from os import listdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from textblob import TextBlob


def split_tweet_data(text, n=30):
    """
    :param text: tweet data
    :param n: number of times the tweets will be randomly grouped
    :return: split list of tweets
    """
    length = len(text)
    size = math.floor(length / n)
    start = np.arange(0, length, size)
    # putting the split tweets into a list
    split_tweets = []
    for piece in range(n):
        split_tweets.append(text[start[piece]:start[piece] + size])
    return split_tweets


class mood:
    def __init__(self):
        run = self.check()
        if run == 0:
            self.sentiment()
        else:
            print("Textual analysis Error")

    def check(self):
        # search for presence of file
        files = [f for f in listdir('../pickles') if isfile(join('../pickles', f))]
        for file in files:
            x = 0
            if file != "corpus.pkl":
                x += 1
                continue
            elif file != "corpus.pkl" and x == len(files):
                return "none"
            else:
                x = 0
                return x

    def datafile(self):
        # Using the initial corpus for sentimental analysis of the tweets
        df = pd.read_pickle('../pickles/corpus.pkl')
        return df

    def pol(self):
        data = self.datafile()
        # getting the polarity of the texts in tweets
        pol = lambda x: TextBlob(x).sentiment.polarity
        data['polarity'] = data['tweet_data'].apply(pol)
        p = data['polarity']
        return p

    def sub(self):
        data = self.datafile()
        # getting the subjectivity of the texts in tweets
        sub = lambda x: TextBlob(x).sentiment.subjectivity
        data['subjectivity'] = data['tweet_data'].apply(sub)
        s = data['subjectivity']
        return s

    def break_tweets(self):
        data = self.datafile()
        print("Breaking tweets into pieces")
        tweet_pieces = []
        for t in data.tweet_data:
            split = split_tweet_data(t)
            tweet_pieces.append(split)
        return tweet_pieces

    def polarity_change_of_tweet(self):
        """
        generate the plot of semantic change of the target in the tweets
        :param pieces: the list of tweet pieces
        :return: plot image
        """
        pieces = self.break_tweets()
        # polarity of each piece of text
        polarity_tweet_data = []
        for lp in pieces:
            polarity_piece = []
            for p in lp:
                polarity_piece.append(TextBlob(p).sentiment.polarity)
            polarity_tweet_data.append(polarity_piece)
        # print(polarity_tweet_data)
        plt.plot(polarity_tweet_data[0])
        plt.xlabel('<---Recent tweets---------------------Older tweets-->', fontsize=10)
        plt.ylabel('<--Negative--------------------------Positive-->', fontsize=10)
        plt.title("Polarity Change")
        # plt.show()
        # save the plot
        return plt.savefig('../visual/static/Polarity Change.png', transparent=True)  # during testing

    # problem saving plot also adds the previous polarity plot
    def overall_sentiment(self):
        plt.clf()
        plt.rcParams['figure.figsize'] = [10, 8]
        x = self.pol()
        y = self.sub()
        plt.scatter(x, y, color='blue')
        plt.text(x + .001, y + .001, "Target is here ", fontsize=12)
        plt.title('Overall Sentiment Analysis', fontsize=20)
        plt.xlabel('<---Negative--------------------------------Postive-->', fontsize=15)
        plt.ylabel('<--Facts-----------------------------------Opinions-->', fontsize=15)
        # save the scatter plot graph
        # plt.show()
        return plt.savefig('../visual/static/Overall_sentiment.png', transparent=True) # during testing

    def sentiment(self):
        self.polarity_change_of_tweet()
        self.overall_sentiment()
        print("Processed tweet sentimental data")

