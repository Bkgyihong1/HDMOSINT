"""
import all the final data
write a report and add the final data details
"""

from flask import Flask, render_template, redirect, url_for, request
from visual.generator import *

app = Flask(__name__)
# app.config["CACHE_TYPE"] = 'null'

@app.route("/")
@app.route("/report")
def report():

    bio = profile()
    exp = experience()
    edu = education()
    interest = interests()
    skill = skills()
    wiki = notability()
    # importing fame level data
    text = open('../final_data/fame_amount.txt', 'r+')
    content = text.read()
    text.close()
    online = check_time_data()
    loc = check_location_data()
    return render_template('report.html', text=content, presence=wiki, online=online, loc=loc, bio=bio, edu=edu,
                           interest=interest, exp=exp, skill=skill)


@app.route("/location")
def location():
    return render_template('location.html')


def webreport():
    app.run()

