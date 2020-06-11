import json
from os import listdir
from os.path import isfile, join


def education():
    # checking for linkedin intelligence
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "LinkedIn_education.json":
            with open('../raw_data/LinkedIn_education.json', 'r') as f:
                educ = json.load(f)
            return educ
        else:
            educ = 0
            return educ



def experience():
    # checking for linkedin intelligence
    exp = 0
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "LinkedIn_experience.json":
            with open('../raw_data/LinkedIn_experience.json', 'r') as f:
                exp = json.load(f)
            break
        else:
            continue
    return exp


def interests():
    # checking for linkedin intelligence
    interest = 0
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "LinkedIn_interests.json":
            with open('../raw_data/LinkedIn_interests.json', 'r') as f:
                interest = json.load(f)
            break
        else:
            continue
    return interest


def skills():
    # checking for linkedin intelligence
    skill = 0
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "LinkedIn_skills.json":
            with open('../raw_data/LinkedIn_skills.json', 'r') as f:
                skill = json.load(f)
            break
        else:
            continue
    return skill


def profile():
    # checking for linkedin intelligence
    prof = 0
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "LinkedIn_profile.json":
            with open('../raw_data/LinkedIn_profile.json', 'r') as f:
                prof   = json.load(f)
            break
        else:
            continue
    return prof


def notability():
    # checking for wiki presence; search for presence of file
    presence = "Target isn't notable enough to have their own wiki page"
    files = [f for f in listdir('../raw_data') if isfile(join('../raw_data', f))]
    for file in files:
        if file == "notability.json":
            with open('../raw_data/notability.json', 'r') as f:
                note = json.load(f)
            nb = str(note[0])
            if nb == "Target isn't notable":
                break
            elif nb == "Target is notable":
                presence = "Target is notable enough, they have their own wiki page"
                break
            else:
                presence = "Not sure if this target is notable ..."
                break
    return presence


def check_time_data():
    # checking for online intelligence
    ins_time = 0
    files = [f for f in listdir('../visual/static') if isfile(join('../visual/static', f))]
    for file in files:
        if file == "Post Timing.png":
            ins_time = 1
            break
        else:
            continue
    return ins_time


def check_location_data():
    # checking for location intelligence
    ins_loc = 0
    files = [f for f in listdir('../visual/static') if isfile(join('../visual/static', f))]
    for file in files:
        if file == "loc_wordcloud.png":
            ins_loc = 1
            break
        else:
            continue
    return ins_loc
