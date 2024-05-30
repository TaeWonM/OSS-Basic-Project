import json
import datetime as dt


# This method makes json file for recode
# It contains times and exercise recodes
def get_statious():
    # variable that contains time data
    now = dt.datetime.now()
    # variable that contains recodes which is in json file
    health_data = []
    flag = False
