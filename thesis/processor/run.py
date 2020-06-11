from thesis.processor import EDAtweets, tweet_sentiment, tweet_topics, igtime, iglocations, fame_level


def ke_run():
    # Processing data
    EDAtweets.wordcloud_generate()  # EDA
    tweet_sentiment.sentiment()  # Sentiment analysis
    tweet_topics.topics()  # Topic generation
    igtime.time_graph(igtime.search())  # possible online presence
    iglocations.loc_cloud(iglocations.check())  # possible location names
    fame_level.popularity()  # level of fame
