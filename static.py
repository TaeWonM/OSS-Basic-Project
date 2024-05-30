import json
import datetime as dt


# This method makes json file for recode
# It contains times and exercise recodes
def get_statious():
    # variable that contains time data
    now = dt.datetime.now()
    # variable that contains recodes which is in json file
    health_data = []
    # variable to check current date
    flag = False
    #Add try statement for exception 
    try:
        # statement to open staticsitc.json file
        with open("staticsitc.json", "r", encoding="utf-8-sig") as json_file:
            # statement to get recodes in staticsitc.json file and find current date
            health_data = json.load(json_file)
            for i in range(0, len(health_data)):
                if (
                    health_data[i]["year"] == now.year
                    and health_data[i]["month"] == now.month
                    and health_data[i]["day"] == now.day
                ):
                    flag = True