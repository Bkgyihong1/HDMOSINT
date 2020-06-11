import json
import re
from os import listdir
from os.path import isfile, join


class fame:
    def __init__(self):
        tw = self.twcheck()
        ig = self.igcheck()
        if tw == 0 and ig == 0:
            self.popularity()
            print("Processed the level of fame")
        else:
            print("Fame calculation Error")

    def igcheck(self):
        # search for presence of file
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            y = 0
            if file != "IGprofile_data.json":
                y += 1
                continue
            elif file != "IGprofile_data.json" and y == len(files):
                return "none"
            else:
                y = 0
                return y

    def twcheck(self):
        # search for presence of file
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            x = 0
            if file != "twitter_profile.json":
                x += 1
                continue
            elif file != "twitter_profile.json" and x == len(files):
                return "none"
            else:
                x = 0
                return x

    def level_of_fame(self, followers):
        # level of fame
        if 100 < followers < 1000:
            result = "target is not famous and probably unknown in the community"
        elif 1000 < followers < 10000:
            result = "target is known in the community"
        elif 10000 < followers < 100000:
            result = "target is most probably known around the country"
        elif 100000 < followers < 500000:
            result = "target is known for their content"
        elif 500000 < followers < 1000000:
            result = "target is a budding celebrity"
        elif 1000000 < followers < 10000000:
            result = "target is Famous and probably an influencer"
        elif 10000000 < followers < 50000000:
            result = "target is a definite influencer"
        elif followers > 50000000:
            result = "almost everyone knows this person"
        else:
            result = "barely anyone knows this person"

        return result

    def interest_circle(self, following, tfollowing):
        """comparing the followers and following
        to know the number of people the target is interested in"""
        if following > tfollowing:
            int_circle = following
        else:
            int_circle = tfollowing

        return int_circle

    def social_circle(self, followers, following, tfollowers, tfollowing):
        # getting the number of interested pages for ins
        if following < followers:
            social_no1 = following
        else:
            social_no1 = followers

        # getting the number of interested pages for twitter
        if tfollowing < tfollowers:
            social_no2 = tfollowing
        else:
            social_no2 = tfollowers

        social_no = ((social_no1/6) + (social_no2/6)) / 2

        return social_no

    def followers_size_check(self):
        with open("../raw_data/IGprofile_data.json", "r") as f:
            profile = json.load(f)
        followers_no = profile['followers']
        x = len(followers_no) - 1

        if followers_no[-1] == 'm':
            f = followers_no[: x]
            f = re.sub('[.]', '', f)
            followers = int(f) * 1000000

        elif followers_no[-1] == 'k':
            f = followers_no[: x]
            f = re.sub('[.]', '', f)
            followers = int(f) * 1000
        else:
            followers_no = re.sub('[,]', '', followers_no)
            followers = int(followers_no)
        return followers

    def following_size_check(self):
        with open("../raw_data/IGprofile_data.json", "r") as f:
            profile = json.load(f)
        following_no = profile['following']
        x = len(following_no) - 1

        if following_no[-1] == 'm':
            f = following_no[: x]
            f = re.sub('[.]', '', f)
            following = int(f) * 1000000

        elif following_no[-1] == 'k':
            f = following_no[: x]
            f = re.sub('[.]', '', f)
            following = int(f) * 1000
        else:
            following_no = re.sub('[,]', '', following_no)
            following = int(following_no)
        return following


    def popularity(self):
        followers_no = self.followers_size_check()
        following_no = self.following_size_check()

        with open("../raw_data/twitter_profile.json", "r") as f:
            tprofile = json.load(f)

        tfollowers_no = int(tprofile['followers'])
        tfollowing_no = int(tprofile['following'])

        # calculations
        insresult = self.level_of_fame(followers_no)
        tresult = self.level_of_fame(tfollowers_no)
        circle_no = int(self.interest_circle(following_no, tfollowing_no))
        friends = int(self.social_circle(followers_no, following_no, tfollowers_no, tfollowing_no))

        # need to store the result into a text file
        with open("../final_data/fame_amount.txt", "w") as fame:
            fame.write("In Instagram, we concluded that " + insresult + ".\n")
            fame.write("From Twitter, we noted that " + tresult + ".\n")
            fame.write("Target is at most interested in " + str(circle_no) + " people on social media, \n")
            fame.write("the highest assumption of the people close to the target is " + str(friends) + "\n")
