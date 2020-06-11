"""
processing the clean tweet data collected the target is finding the
Most common words tweeted; Size of vocabulary they usually use;
Amount of profanity in their vocabulary
"""
import json
from os import listdir
from os.path import isfile, join

import pandas as pd
import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer


class EDA:
    def __init__(self):
        run = self.check()
        if run == 0:
            self.wordcloud_generate()
        else:
            print("Couldn't process target vocabulary")

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

    def eda_start(self):
        with open('../raw_data/tweets.json', 'r') as f:
            tweet_data = json.load(f)
        tweet = tweet_data['tweets']

        # getting the most common words tweeted
        content = pd.read_pickle("../pickles/dtm.pkl")
        content = content.transpose()
        return content

    def wordcloud_generate(self):
        # First update our document-term matrix with the new list of stop words
        # Read in cleaned data
        data_clean = pd.read_pickle('../pickles/data_clean.pkl')
        # Add new stop words
        add_stop_words = ['just', 'im']
        stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
        # Recreate document-term matrix
        cv = CountVectorizer(stop_words=stop_words)
        data_cv = cv.fit_transform(data_clean.tweet_data)
        data_stop = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_stop.index = data_clean.index

        # Pickle it for later use
        pickle.dump(cv, open("../pickles/cv_stop.pkl", "wb"))
        data_stop.to_pickle("../pickles/dtm_stop.pkl")
        # now we make the word cloud
        wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2", max_font_size=150,
                       random_state=42)
        data = self.eda_start()
        # setting the output of the wordcloud
        plt.rcParams['figure.figsize'] = [8, 8]

        for index, target in enumerate(data.columns):
            wc.generate(data_clean.tweet_data[target])
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title("Main tweet contents: ")

        # plt.show() # prints out the wordcloud of the person
        # saves the generated wordcloud to an image.png in final_data
        wc.to_file("../visual/static/wordcloud.png") # during testing
        plt.clf()
        print("Processed EDA on tweet data")