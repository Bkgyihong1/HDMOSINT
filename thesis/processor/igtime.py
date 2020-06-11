"""
collect the different times of the IG posts
calculate the most occuring time zone:
morning, afternoon, night
for most posts
Intelligence = assumed time when user is on the phone
"""

import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


class time_plot:
    def __init__(self):
        print("Running IG time data")

        self.time_graph()

    def search(self):
        # search for presence of file
        igTime = 0
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            if file != "IGtimestamps.json":
                continue
            else:
                # extract timestamp from the json data into a list of timestamps
                with open("../raw_data/IGtimestamps.json", "r") as f:
                    igtime = json.load(f)
                # print(igtime)
                igTime = []
                for index in igtime:
                    x = str(index)
                    data = igtime[x]
                    time_data = list(data.values())
                    igTime.append(time_data[0])
        return igTime

    def time_graph(self):
        igt = self.search()
        if igt == 0:
            print("Online Presence data error")
        else:
            if igt == "no timestamps":
                print("Failed to process timestamps data")
            else:
                # getting the datetime from timestamp
                igdatetime = []  # list of datetime data
                x = 0
                while x != 12:
                    # 12 because we are only able to collect 12 posts at the moment
                    timestampn = datetime.fromtimestamp(int(igt[x]))
                    igdatetime.append(timestampn)
                    x += 1
                # putting datetime data into a dataframe
                igtime_df = pd.DataFrame(data=igdatetime, columns=['Datetime'])
                igtime_df['date'] = igtime_df['Datetime'].dt.date
                igtime_df['time'] = igtime_df['Datetime'].dt.time
                igtime_df['hour_of_day'] = igtime_df['Datetime'].dt.hour

                # plot the scatterplot of times against the post
                date = list(igtime_df['date'])
                time_hour = list(igtime_df['hour_of_day'])
                x = time_hour
                y = date
                # plot
                plt.clf()
                plt.rcParams['figure.figsize'] = [8, 8]
                plt.plot([], [])
                plt.scatter(x, y)
                plt.xlabel('<-----------24 hour based--------------->', fontsize=10)
                plt.ylabel('<------OLDER--------Post dates--------LATEST--------->', fontsize=10)
                plt.title("Scatter Plot of Target's Posting Time")
                #plt.show()
                plt.savefig('../visual/static/Post Timing.png', transparent=True)  # during testing
                print("Processed IG time data")

    ''' 
    # find the most occuring range of time based on morning, afternoon, evening or night
    def time_of_day(self, m, a, e, n, ln):
        if m > a and m > e and m > n and m > ln:
            message = "Target usually posts in the mornings"
        elif a > m and a > e and a > n and a > ln:
            message = "Target usually posts in the afternoons"
        elif e > m and e > a and e > n and e > ln:
            message = "Target usually posts in the evenings"
        elif n > m and n > a and n > e and n > ln:
            message = "Target usually posts in the night"
        else:
            message = "Target usually posts late in the night"
        return message
        
    time_hr = list(igtime_df['hour_of_day'])  # call the hour_of_day into a list
    index = 0
    morning = 0
    afternoon = 0
    evening = 0
    night = 0
    late_night = 0
    while index < 12 in time_hr:
        hr = time_hr[index]
        if 6 <= hr <= 11:
            morning = morning + 1
        elif 12 <= hr <= 16:
            afternoon = afternoon + 1
        elif 17 <= hr <= 20:
            evening = evening + 1
        elif 21 <= hr <= 24:
            night = night + 1
        else:
            late_night = late_night + 1
        index += 1
    online_time = time_of_day(morning, afternoon, evening, night, late_night)
    '''

