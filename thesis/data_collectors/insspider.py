from bs4 import BeautifulSoup
import json
import requests
import random
import time


class InstagramOSINT:

    def __init__(self, username):
        self.useragents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

        self.username = username
        # Make the directory that we are putting the files into
        print(f"Starting Scan on {self.username}")
        # Get the html data with the requests module
        r = requests.get(f'http://instagram.com/{self.username}',
                         headers={'User-Agent': random.choice(self.useragents)})
        soup = BeautifulSoup(r.text, features="html.parser")
        # To prevent a unicode error, we need the following line...
        soup.encode('utf-8')
        # Find the tags that hold the data we want to parse
        general_data = soup.find_all('meta', attrs={'property': 'og:description'})
        more_data = soup.find_all('script', attrs={'type': 'text/javascript'})
        description = soup.find('script', attrs={'type': 'application/ld+json'})

        # Try to parse the content -- if it fails then the program exits
        try:
            self.text = general_data[0].get('content').split()
            # This is the profile description data
            self.description = json.loads(description.string)
            # This is the javascript json that is passed into json.loads()
            self.profile_meta = json.loads(more_data[3].string[21:].strip(';'))
            self.profile_data = {
                "Username": self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
                "Profile name": self.description['name'],
                "URL": self.description['mainEntityofPage']['@id'],
                "followers": self.text[0], "following": self.text[2], "Posts": self.text[4],
                "Bio": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['biography']),
                "profile_pic_url": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                           'profile_pic_url_hd']),
                "is_business_account": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                        'is_business_account']),
                "connected_to_fb": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                           'connected_fb_page']),
                "externalurl": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
                "joined_recently": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                           'is_joined_recently']),
                "business_category_name": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                        'business_category_name']),
                "is_private": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
                "is_verified": str(
                    self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}

            # Tries to scrape posts if it is a public profile
            self.save_data()
            self.scrape_posts()
            print("")
        except Exception as e:
            print(e)
            print(f"Username {self.username} not found")

    def scrape_posts(self):
        if self.profile_data['is_private'].lower() == 'true':
            print("[*]Private page, cannot scrape photos!")
        else:
            posts = {}
            print("Searching posted images")
            # Downloads the thumbnails of the post
            # Picture is just an int index of the url in the list
            if self.profile_data['is_private'].lower() == 'true':
                print("[*]Private page, cannot scrape photos!")
            else:

                for index, post in enumerate(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                 'edge_owner_to_timeline_media']['edges']):
                    i = str(index)
                    try:
                        posts[index] = {
                            "Caption": str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
                            "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                            "Comments Disabled": str(post['node']['comments_disabled']),
                            "Number of Likes": str(post['node']['edge_liked_by']['count']),
                            "Accessability Caption": str(post['node']['accessibility_caption'])
                        }
                    except IndexError:
                        posts[index] = {"Caption": 'Null',
                                        "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                                        "Comments Disabled": str(post['node']['comments_disabled']),
                                        "Number of Likes": str(post['node']['edge_liked_by']['count']),
                                        "Accessability Caption": str(post['node']['accessibility_caption'])
                                        }
                    with open('picture_' + i + '.jpg', 'wb') as pictures:
                        time.sleep(random.randint(5, 10))
                        r = requests.get(post['node']['thumbnail_resources'][0]['src'],
                                         headers={'User-Agent': random.choice(self.useragents)})
                        # Takes the content of r and puts it into the file
                        pictures.write(r.content)

    def save_data(self):
        # SAVES POST INFORMATION
        posts = {}
        timestamp = {}
        locations = {}
        if self.profile_data['is_private'].lower() == 'true':
            print("[*]Private page, cannot scrape photos!")
        else:
            for index, post in enumerate(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                             'edge_owner_to_timeline_media']['edges']):
                i = str(index)
                try:
                    posts[index] = {
                        "Caption": str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
                        "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                        "Comments Disabled": str(post['node']['comments_disabled']),
                        "Number of Likes": str(post['node']['edge_liked_by']['count']),
                        "Accessability Caption": str(post['node']['accessibility_caption'])
                        }
                except IndexError:
                    posts[index] = {"Caption": 'Null',
                                    "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                                    "Comments Disabled": str(post['node']['comments_disabled']),
                                    "Number of Likes": str(post['node']['edge_liked_by']['count']),
                                    "Accessability Caption": str(post['node']['accessibility_caption'])
                                    }
                timestamp[index] = {'timestamp': str(post['node']['taken_at_timestamp'])}
                locations[index] = {"location": str(post['node']['location'])}

            with open(f"IGposts_data.json", 'w') as f:
                json.dump(posts, f)
            with open(f"IGtimestamps.json", 'w') as f:
                json.dump(timestamp, f)
            with open(f"IGlocations.json", 'w') as f:
                json.dump(locations, f)
            print("Finished")
        with open('IGprofile_data.json', 'w') as f:
            f.write(json.dumps(self.profile_data))

