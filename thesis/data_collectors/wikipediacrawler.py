import urllib.request
import urllib.error
import json

'''
import sys
import requests
from bs4 import BeautifulSoup
'''


class WikiPage:
    def __init__(self, firstname, surname):
        self.name = f'{firstname}' + '_' + f'{surname}'
        url = f"https://en.wikipedia.org/wiki/{self.name}"
        self.url = url
        wiki = []
        try:
            page = urllib.request.urlopen(url)  # connect to the website
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
            print("Sorry this person doesn't have a wiki page")
            result = "Target isn't notable"
            wiki.append(result)
            with open(f'../raw_data/notability.json', 'w') as f:
                json.dump(wiki, f)

        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            print("Sorry couldn't connect to wiki page")
            result = "Connection problems, not sure if the target is notable"
            wiki.append(result)
            with open(f'../raw_data/notability.json', 'w') as f:
                json.dump(wiki, f)

        else:
            # 200
            # ...
            page
            print("Found the wiki page")
            result = "Target is notable"
            wiki.append(result)
            with open(f'../raw_data/notability.json', 'w') as f:
                json.dump(wiki,f)

        return
            # self.bio_collection()
            # self.page_content()

    '''def bio_collection(self):
        page = requests.get(self.url)  # connecting to target page
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table')
        row = table.find_all('tr')
        # print("----------BIOGRAPHY---------")
        print("----------getting biography---------")
        bio = {}
        index = 0
        for row in row:
            bio_data = row.get_text().split('\n')
            bio[index] = bio_data
            index += 1
        with open(f'../raw_data/Wiki_Bio.json', 'w') as f:
            json.dump(bio, f, indent=4)

    def page_content(self):
        page = requests.get(self.url)  # connecting to target page
        soup = BeautifulSoup(page.text, 'html.parser')
        gossip = soup.find_all('p')
        # print("----------PAGE GOSSIP---------")
        print("----------getting page content---------")
        with open(f'../raw_data/Wiki_content.txt', 'w') as f:
            for gossip in gossip:
                content = gossip.get_text()
                f.write(content)'''
