import time

start = time.time()
from thesis.data_collectors import crawler
from thesis.preprocessor import tweets, loc_bot
from thesis.processor import EDAtweets, tweet_sentiment, tweet_topics, fame_level, igtime, iglocations, report

# Collecting target data
crawler = crawler.Crawler()

# Preprocessing data
twt_c = tweets.preprocess_tweets()
cc = loc_bot.Coordinates()

# processing and analysis
eda = EDAtweets.EDA()  # EDA
sentiment = tweet_sentiment.mood()  # Sentiment analysis
topics = tweet_topics.ldatopics()  # Topic generation
online = igtime.time_plot()  # possible online presence
location_cloud = iglocations.loc_wc()  # possible location names
popular = fame_level.fame()  # level of fame

# Completion notice
print("SYSTEM EXECUTION SUCCESSFUL")
end = time.time()
print("Execution time:", end - start, "seconds")
# Report generation
report.report_view()
