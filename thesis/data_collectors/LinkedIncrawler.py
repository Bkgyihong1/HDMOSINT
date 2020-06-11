import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from webdriver_manager.chrome import ChromeDriverManager

SCROLL_PAUSE_TIME = 10
BREAK_TIME = 3
REST = 4


class LinkedInCrawl:
    def __init__(self, url):
        if url == 'None' or 'none':
            print("")
        self.link = "https://www.linkedin.com/in/" + url  # link of person who will be scraped
        self.connectL()

    def connectL(self):
        # browser = webdriver.Chrome('C:/webdrivers/chromedriver.exe')
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get('https://www.linkedin.com/login')
        time.sleep(BREAK_TIME)
        browser.find_element_by_id('username').send_keys(
            'EMAIL')  # Enter email of linkedin account here
        time.sleep(BREAK_TIME)
        browser.find_element_by_id('password').send_keys('PASSWORD')  # Enter Password of linkedin account here
        time.sleep(REST)
        browser.find_element_by_xpath("//*[@type='submit']").click()
        time.sleep(BREAK_TIME)
        browser.get(self.link)

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        for i in range(3):
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # scraping LinkedIn details now
        time.sleep(BREAK_TIME)
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')

        name_div = soup.find('div', {'class': 'flex-1 mr5'})
        name_loc = name_div.find_all('ul')
        name = name_loc[0].find('li').get_text().strip()
        loc = name_loc[1].find('li').get_text().strip()
        profile_title = name_div.find('h2').get_text().strip()
        connection = name_loc[1].find_all('li')
        connection = connection[1].get_text().strip()

        # profile data
        profile = []
        info = {
            "Name": name,
            "Location": loc,
            "Position": profile_title,
            "Connections": str(connection) + " in Linkedin"

        }
        profile.append(info)

        with open('../raw_data/LinkedIn_profile.json', 'w') as pfile:
            json.dump(profile, pfile)

        # experience data
        print("Searching for information on target claimed experience")
        try:
            exp_section = soup.find('section', {'id': 'experience-section'}).find('ul')
            work_place = exp_section.find_all('li', {
                'class': 'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})

            experience_data = []

            for work_place in work_place:
                position = work_place.find('h3').get_text().strip()
                company = work_place.find('p',
                                          {
                                              'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip()
                duration = work_place.find('h4', {
                    'class': 'pv-entity__date-range t-14 t-black--light t-normal'}).get_text().strip()
                experience_content = {
                    "Position": position,
                    "Company": company,
                    "Time": duration
                }
                experience_data.append(experience_content)

            with open('../raw_data/LinkedIn_experience.json', 'w') as expfile:
                json.dump(experience_data, expfile)

        except:
            print("Failed to collect experience data")
            experience_data = ['No experience data']
            with open('../raw_data/LinkedIn_experience.json', 'w') as expfile:
                json.dump(experience_data, expfile)

        # education data
        print("Searching for information on target claimed education")
        try:
            edu_section = soup.find('section', {'id': 'education-section'}).find('ul')
            schools = edu_section.find_all('li', {
                'class': 'pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view'})
            education_data = []

            for schools in schools:
                place = schools.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'}).get_text().strip()
                major = schools.find('p',
                                     {
                                         'class': 'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'})
                major_name = major.find('span', {'class': 'pv-entity__comma-item'}).get_text().strip()
                time_edu = schools.find('p',
                                        {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).get_text().strip()
                education_content = {
                    "school": place,
                    "major": major_name,
                    "Time": time_edu
                }
                education_data.append(education_content)

            with open('../raw_data/LinkedIn_education.json', 'w') as edufile:
                json.dump(education_data, edufile)

        except:
            print("Failed to collect education data")
            education_data = ['No education data']
            with open('../raw_data/LinkedIn_education.json', 'w') as edufile:
                json.dump(education_data, edufile)

        # interest data
        print("Searching for information on target claimed interest")
        try:
            interest_section = soup.find('section', {
                'class': 'pv-profile-section pv-interests-section artdeco-container-card ember-view'}).find('ul')
            interests = interest_section.find_all('li')
            interests_data = []
            for interests in interests:
                interest = interests.find('h3', {
                    'class': 'pv-entity__summary-title t-16 t-16--open t-black t-bold'}).get_text().strip()
                interests_data.append(interest)

            with open('../raw_data/LinkedIn_interests.json', 'w') as ifile:
                json.dump(interests_data, ifile)

        except:
            print("Failed to collect LinkedIn interests")
            interests_data = ['No interest data']
            with open('../raw_data/LinkedIn_interests.json', 'w') as ifile:
                json.dump(interests_data, ifile)

        # skills
        print("Searching for information on target claimed skills")
        try:
            skills_section = soup.find('section', {
                "class": 'pv-profile-section pv-skill-categories-section artdeco-container-card ember-view'}).find('ol')
            skills_names = skills_section.find_all('li')
            skills_data = []
            for skills_names in skills_names:
                skill_name = skills_names.find('span', {
                    'class': 'pv-skill-category-entity__name-text t-16 t-black t-bold'}).get_text().strip()
                skills_data.append(skill_name)

                with open('../raw_data/LinkedIn_skills.json', 'w') as sfile:
                    json.dump(skills_data, sfile)
        except:
            print("Failed to collect LinkedIn skills")
            skills_data = ['No skill data']
            with open('../raw_data/LinkedIn_skills.json', 'w') as sfile:
                json.dump(skills_data, sfile)

        browser.quit()
        print("Successfully saved LinkedIn Details in " + (os.getcwd()))

