"""
extract location names and save to list
connect to online search for latitude and longitude of each loc
save latitude and longitude to individual  list separately
add the lat_long lists into one dictionary??
"""
import json
import time
import string
import re
from os import listdir
from os.path import isfile, join

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class Coordinates:
    def __init__(self):
        run = self.check()
        if run == 0:
            self.coordinatecollect(loc_details=self.loc_names())
        else:
            print("No location cordinates")

    def check(self):
        # search for presence of file
        files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
        for file in files:
            x = 0
            if file != "IGlocations.json":
                x += 1
                continue
            elif file != "IGlocations.json" and x == len(files):
                return "none"
            else:
                x = 0
                return x


    def loc_data(self):
        with open('../raw_data/IGlocations.json', 'r') as loc:
            loc_raw = json.load(loc)
        # print(loc_raw)

        # extract the values of location in json file
        loc_rawdetails = []
        for index in loc_raw:
            x = str(index)
            data = loc_raw[x]
            details = list(data.values())
            loc_rawdetails.append(details[0])
        return loc_rawdetails

    def loc_names(self):
        # check for the names of the location, if None then skip
        loc = self.loc_data()
        loc_details = []
        for x in loc:
            if x == 'None':
                continue
            else:
                x = x.lower()
                x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)
                x = re.sub(r'id.+slug', '', x)
                x = x.strip()
                if x.isspace():
                    continue
                else:
                    loc_details.append(x)
        return loc_details

    def coordinatecollect(self, loc_details):
        # search and collect the latitude and longitude of the locations
        geo_coordinates = []  # list of geo data
        # browser = webdriver.Chrome('C:/webdrivers/chromedriver.exe')
        browser = webdriver.Chrome(ChromeDriverManager().install())
        for x in loc_details:
            if x == '':
                continue
            else:
                link = 'https://nominatim.openstreetmap.org'
                browser.get(link)
                time.sleep(2)
                browser.find_element_by_name('q').send_keys(x)
                browser.find_element_by_name('q').send_keys(Keys.ENTER)
                try:
                    browser.find_element_by_xpath('//*[@id="searchresults"]/div[1]/a').click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    table = soup.find('table')
                    row = table.find_all('tr')
                    geo_loc = row[7].get_text()
                    if geo_loc.startswith('OSM'):
                        geo_loc = row[6].get_text()
                    # cleaning geo points collected
                    geo_loc = re.sub(r'Centre Point', '', geo_loc)
                    geo_coordinates.append(geo_loc)
                except NoSuchElementException:
                    print("Couldn't collect GPS coordinates")
        # print(geo_coordinates)

        with open('C:/Users/Kembabazi Barbara/Desktop/Cesium/coordinates.json', 'w') as fc:
            json.dump(geo_coordinates, fc)
        browser.quit()

