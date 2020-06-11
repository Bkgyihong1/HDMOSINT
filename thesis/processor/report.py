import os
from visual.report import webreport


def report_view():
    ans = input("Do you want to see the final report? Enter y for yes: ")
    if ans == 'y':
        # run the flask report generator
        os.chdir("../visual")
        webreport()
    else:
        print("Please check path " + os.getcwd() + "\ final_data for the intelligence data")