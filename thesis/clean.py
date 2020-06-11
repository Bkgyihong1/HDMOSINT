"""
cleaning the local directory of final data
so as to prevent mixing different target data together
before system run
"""
import os

def clean_folders():
    os.rmdir("../final_data")
    os.rmdir("../raw_data")
    os.rmdir("../pickles")
    os.rmdir("../clean_data")
    os.mkdir("../final_data")
    os.mkdir("../raw_data")
    os.mkdir("../pickles")
    os.mkdir("../clean_data")
    print("Cleaned folders")


clean_folders()