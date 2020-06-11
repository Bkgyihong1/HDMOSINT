"""
classify the tweets to figure out what topics the target tends to discuss on twitter
topic generation from the tweets using Latent Dirichlet Allocation (LDA)
"""
import re
import string
from os import listdir
from os.path import isfile, join

import pandas as pd
import pickle
import scipy.sparse
import matplotlib.pyplot as plt

from gensim import matutils, models  # needed for LDA
from nltk import word_tokenize, pos_tag
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud


class ldatopics:
    def __init__(self):
        run = self.check()
        if run == 0:
            x = 0
            if x != 2:
                self.topics()
                x += 1
        else:
            print("Textual analysis Error")
        print("Processed topics data")

    def check(self):
        # search for presence of file
        files = [f for f in listdir('../pickles') if isfile(join('../pickles', f))]
        for file in files:
            x = 0
            if file != "dtm_stop.pkl":
                x += 1
                continue
            elif file != "dtm_stop.pkl" and x == len(files):
                return "none"
            else:
                x = 0
                return x

    def clean_text(self, content):  # cleaning the topic contents
        """
        Make text lowercase,
        remove punctuation and
        remove words containing numbers.
        """
        content = content.lower()
        content = re.sub('[%s]' % re.escape(string.punctuation), '', content)
        content = re.sub('\w*\d\w*', '', content)
        content = re.sub(r'\w+id\s', '', content)
        content = re.sub(r'\w+none\s?', '', content)
        return content

    def nouns(self, tweets):
        """
        pull out nouns from the string of text
        using nouns to determine the topics
        :param tweets: tokenize the tweets and pull out only nouns
        :return: nouns
        """
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = word_tokenize(tweets)
        all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)]
        return ' '.join(all_nouns)

    def topics(self):
        """
        first try / test
        putting tdm into gensim format to be used for LDM
        df -> sparse matrix -> gensim corpus
        """
        data = pd.read_pickle('../pickles/dtm_stop.pkl')
        tdm = data.transpose()
        cv = pickle.load(open("../pickles/cv_stop.pkl", "rb"))

        # Cleaning data
        data_clean = pd.read_pickle('../pickles/data_clean.pkl')
        data_nouns = pd.DataFrame(data_clean.tweet_data.apply(self.nouns))  # applying the noun function to data
        # creating new document- term matrix containing only the nouns
        add_stop_words = ['like', 'im', 'know', 'right', 'dont', 'thats', 'day', 'years', 'got', 'gonna', 'night',
                          'think', 'yeah', 'said', 'tomorrow', 'today', 'pst']
        stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
        # cv stands for count vector
        cvn = CountVectorizer(stop_words=stop_words)
        data_cvn = cvn.fit_transform(data_nouns.tweet_data)
        data_dtmn = pd.DataFrame(data_cvn.toarray(), columns=cvn.get_feature_names())
        data_dtmn.index = data_nouns.index
        # print(data_dtmn)

        """
        putting tdm into gensim format to be used for LDM
        df -> sparse matrix -> gensim corpus
        """
        sparse_ncounts = scipy.sparse.csr_matrix(data_dtmn.transpose())
        corpusn = matutils.Sparse2Corpus(sparse_ncounts)
        id2wordn = dict((v, k) for k, v in cvn.vocabulary_.items())
        # Our final LDA model (for now)
        ldan = models.LdaModel(corpus=corpusn, id2word=id2wordn, num_topics=5, passes=10)
        # print(ldan.print_topics())


        # saving the topics collected into a txt file
        with open('../raw_data/topics.txt', 'w') as topic_file:
            topics = ldan.top_topics(corpusn)
            topic_file.write('\n'.join('%s %s' %topic for topic in topics))

        with open('../raw_data/topics.txt', 'r') as topic_file:
            topics = topic_file.read()

        topic_data = {'topics': self.clean_text(topics)}
        # print(topic_data)

        data_df = pd.DataFrame(topic_data, index=['topics']).transpose()
        data_df.columns = ['topics_collected']
        data_df = data_df.sort_index()
        # print(data_df)
        # print(data_df.topics_collected.loc['topics'])

        # counting the occurrence of topics in a document term matrix
        cv = CountVectorizer()

        data_cv = cv.fit_transform(data_df.topics_collected)
        # Convert it to an array and label all the columns
        # Can use this part for future projects
        topic_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        topic_dtm.index = data_df.index

        # print(topic_dtm)  # Document-Term Matrix
        # present the topics in a word cloud
        word = data_df.topics_collected['topics']
        wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2", max_font_size=150, random_state=42)
        wc.generate(word)
        plt.clf()
        plt.rcParams['figure.figsize'] = [8, 8]
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Topics Generated")
        # plt.show() # prints out the wordcloud of the person
        # saves the generated wordcloud to an image.png in final_data
        wc.to_file("../visual/static/topic_wordcloud.png")  # during testing