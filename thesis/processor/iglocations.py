"""
extract the locations tagged on IG posts
"""
import json
import re
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


class loc_wc:
    def __init__(self):
        print("Creating location wordcloud")
        self.loc_cloud()

    def clean_text(self,content):
        """
        Make text lowercase,
        remove punctuation and
        remove words containing numbers.
        """
        content = content.lower()
        content = re.sub('[%s]' % re.escape(string.punctuation), ' ', content)
        content = re.sub('\w*\d\w*', '', content)
        content = re.sub(r'\w+id\s', '', content)
        content = re.sub(r'\w+none\s?', '', content)
        return content

    def check(self):
        # search for presence of file
        locdetail = 0
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            x = 0
            y = 6
            if file != "IGlocations.json":
                continue
            else:
                with open("../raw_data/IGlocations.json", "r") as f:
                    iglocation = json.load(f)
                locdetail = []
                for index in iglocation:
                    x = str(index)
                    data = iglocation[x]
                    details = list(data.values())
                    locdetail.append(details[0])
        return locdetail

    def loc_cloud(self):
        """
        convert to document term matrix
        """
        locdetails = self.check()
        if locdetails == 0:
            print("Target location processing Error")
        else:
            with open('../clean_data/igloc.txt', 'w') as file:
                for detail in locdetails:
                    detail = re.sub("([^\x00-\x7F])+", " ", detail)
                    file.write(detail)

            with open('../clean_data/igloc.txt', 'r') as file:
                location = file.read().replace("\n", " ")
                file.close()

            loc_data = {'location': self.clean_text(location)}
            # print(loc_data)
            """
            create a document-term matrix using CountVectorizer,
            and exclude common English stop words
            """
            data_df = pd.DataFrame(loc_data, index=['location']).transpose()
            data_df.columns = ['loc_data']
            data_df = data_df.sort_index()
            # print(data_df)
            # print(data_df.loc_data.loc['location'])  # corpus of the location data

            # making stop words
            add_stop_words = ['haspublicpage', 'id', 'slug', 'name', 'true', 'false', 'none','public','page']
            stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
            # making document term matrix
            cv = CountVectorizer(stop_words=stop_words)
            if loc_data['location'] == '':
                print("No location found")
            else:
                data_cv = cv.fit_transform(data_df.loc_data)
                # Convert it to an array and label all the columns
                # Can use this part for future projects
                loc_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
                loc_dtm.index = data_df.index

                places = data_df.loc_data['location']
                wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2", max_font_size=150,
                               random_state=42)
                wc.generate(places)
                plt.clf()
                plt.rcParams['figure.figsize'] = [8, 8]
                plt.imshow(wc, interpolation="bilinear")
                plt.axis("off")
                plt.title(' Possible Locations Collected ')
                wc.to_file("../visual/static/loc_wordcloud.png")  # during testing