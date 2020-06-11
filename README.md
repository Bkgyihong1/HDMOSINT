This program follows the general workflow of an Open Source Intelligence System to extract behavioural patterns and intelligence on a target social media user:
1. Data Collection
2. Data Processing 
3. Data Analysis

**HOW TO RUN THIS PROGRAM:**
1. Install requirements.txt libraries.

2. Data collection is focused on Social media applications and borrows the techniques used in web crawlers:
    
    Before running the program;
    The user is required to input their login credentials for Linkedin and Twitter API keys 
     in their respective scripts:
     
     LinkedIn = LinkedIncrawler.py
     
     Twitter = twitterspider.py

3. Run main.py file and input the target person's name/username/url requirements are stated:

    The final results are saved separately under ../visual/static folder and final_data folder.

4. Incase of viewing locations on the world map, please install Cesium  separately


NOTE: 
- Change loc_bot.py line 105 path to Cesium directory PATH respectively.
- Place ../visual/templates/loc.py under Cesium Apps folder
- Execute under CMD node sever.cjs

This project is strictly education therefore, use it wisely.
This program is still under development, please feel free to contribute.